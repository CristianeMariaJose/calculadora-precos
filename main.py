import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
import json
import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Importar módulo de banco de dados MongoDB
from database_mongo import load_cadastros, add_cadastro, update_cadastro, get_cadastro_by_email
logger.info("Usando MongoDB Atlas para persistência de dados")

# Importar módulo WhatsApp (se existir)
try:
    from whatsapp_sender import enviar_whatsapp_automatico
    WHATSAPP_DISPONIVEL = True
    logger.info("Módulo WhatsApp carregado com sucesso")
except ImportError:
    WHATSAPP_DISPONIVEL = False
    logger.warning("Módulo WhatsApp não encontrado - funcionalidade desabilitada")

app = Flask(__name__, template_folder=".", static_folder="static")
app.secret_key = "calculadora_marketplaces_secret_key"

@app.route("/")
def landing():
    """Página inicial com landing page comercial."""
    logger.debug("Acessando landing page")
    return render_template("landing_new.html")

@app.route("/app")
def app_index():
    """Página da calculadora (requer licença)."""
    # Verificar se o usuário tem uma licença válida na sessão
    if "licenca" not in session:
        # Redirecionar para a landing page
        logger.debug("Usuário sem licença, redirecionando para landing page")
        return redirect(url_for("landing"))
    
    # Licença válida, mostrar a calculadora
    logger.debug("Usuário com licença, mostrando calculadora")
    return render_template("static/index.html")

@app.route("/admin")
def admin_login():
    """Página de login do painel administrativo."""
    logger.debug("Acessando página de login do admin")
    return render_template("static/admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Painel administrativo para gerenciar cadastros e licenças."""
    # Em produção, verificaria autenticação aqui
    cadastros = load_cadastros()
    logger.debug(f"Acessando dashboard admin, {len(cadastros)} cadastros carregados")
    return render_template("static/admin_dashboard.html", cadastros=cadastros)

@app.route("/upgrade")
def upgrade():
    """Página de upgrade para versão completa."""
    logger.debug("Acessando página de upgrade")
    try:
        return render_template("templates/upgrade.html")
    except:
        # Fallback se o template não existir
        return render_template("static/upgrade.html")

@app.route("/ativar")
def ativar():
    """Página de ativação da licença."""
    return render_template("static/ativar.html")

@app.route("/calculadora")
def calculadora():
    """Página da calculadora de preços para marketplaces."""
   logger.debug("Acessando calculadora de preços - v2")
    return render_template("calculadora.html")

@app.route("/monitor")
def monitor():
    """Página do monitor de preços."""
    return render_template("static/monitor.html")

# ===== APIs =====

@app.route("/api/cadastros", methods=["GET"])
def api_get_cadastros():
    """API para obter todos os cadastros."""
    try:
        cadastros = load_cadastros()
        logger.debug(f"API: Retornando {len(cadastros)} cadastros")
        return jsonify({"success": True, "cadastros": cadastros})
    except Exception as e:
        logger.error(f"API: Erro ao obter cadastros: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    """API para receber cadastros do formulário."""
    try:
        data = request.form
        logger.debug(f"API: Recebendo cadastro: {data}")
        
        # Validação básica
        if not data.get('name') or not data.get('email') or not data.get('whatsapp'):
            logger.warning("API: Dados de cadastro incompletos")
            return jsonify({"success": False, "error": "Todos os campos são obrigatórios"})
        
        # Verificar se o email já existe
        cadastro_existente = get_cadastro_by_email(data.get('email'))
        if cadastro_existente:
            logger.warning(f"API: Email já cadastrado: {data.get('email')}")
            return jsonify({"success": False, "error": "Email já cadastrado"})
        
        # Salvar cadastro usando o módulo de banco de dados
        if add_cadastro(data.get('name'), data.get('email'), data.get('whatsapp')):
            logger.debug(f"API: Cadastro salvo com sucesso para {data.get('email')}")
            return jsonify({"success": True})
        else:
            logger.error("API: Erro ao salvar cadastro")
            return jsonify({"success": False, "error": "Erro ao salvar cadastro"})
            
    except Exception as e:
        logger.error(f"API: Erro no servidor: {e}")
        return jsonify({"success": False, "error": f"Erro no servidor: {str(e)}"})

@app.route("/api/confirmar_pagamento", methods=["POST"])
def api_confirmar_pagamento():
    """API para confirmar pagamento de um cadastro."""
    try:
        data = request.json
        email = data.get('email')
        logger.debug(f"API: Confirmando pagamento para {email}")
        
        # Atualizar o cadastro
        dados_atualizados = {
            "pagamento_confirmado": True,
            "data_confirmacao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if update_cadastro(email, dados_atualizados):
            logger.debug(f"API: Pagamento confirmado para {email}")
            return jsonify({"success": True})
        else:
            logger.error(f"API: Erro ao atualizar cadastro para {email}")
            return jsonify({"success": False, "error": "Erro ao atualizar cadastro"})
            
    except Exception as e:
        logger.error(f"API: Erro ao confirmar pagamento: {e}")
        return jsonify({"success": False, "error": f"Erro no servidor: {str(e)}"})

@app.route("/api/enviar_licenca", methods=["POST"])
def api_enviar_licenca():
    """API para marcar licença como enviada."""
    try:
        data = request.json
        email = data.get('email')
        logger.debug(f"API: Marcando licença como enviada para {email}")
        
        # Atualizar o cadastro
        dados_atualizados = {
            "licenca_enviada": True,
            "data_envio": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if update_cadastro(email, dados_atualizados):
            logger.debug(f"API: Licença marcada como enviada para {email}")
            return jsonify({"success": True})
        else:
            logger.error(f"API: Erro ao atualizar cadastro para {email}")
            return jsonify({"success": False, "error": "Erro ao atualizar cadastro"})
            
    except Exception as e:
        logger.error(f"API: Erro ao marcar licença como enviada: {e}")
        return jsonify({"success": False, "error": f"Erro no servidor: {str(e)}"})

@app.route("/api/enviar_whatsapp", methods=["POST"])
def api_enviar_whatsapp():
    """API para enviar WhatsApp automático."""
    try:
        if not WHATSAPP_DISPONIVEL:
            return jsonify({"success": False, "error": "Módulo WhatsApp não disponível"})
        
        data = request.json
        email = data.get('email')
        logger.debug(f"API: Enviando WhatsApp para {email}")
        
        # Buscar dados do cadastro
        cadastro = get_cadastro_by_email(email)
        if not cadastro:
            return jsonify({"success": False, "error": "Cadastro não encontrado"})
        
        # Enviar WhatsApp
        resultado = enviar_whatsapp_automatico(
            nome=cadastro.get('nome', ''),
            whatsapp=cadastro.get('whatsapp', ''),
            email=email
        )
        
        if resultado['success']:
            # Atualizar cadastro marcando WhatsApp como enviado
            dados_atualizados = {
                "whatsapp_enviado": True,
                "data_whatsapp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            update_cadastro(email, dados_atualizados)
            
            logger.debug(f"API: WhatsApp enviado com sucesso para {email}")
            return jsonify({"success": True, "message": "WhatsApp enviado com sucesso!"})
        else:
            logger.error(f"API: Erro ao enviar WhatsApp para {email}: {resultado['error']}")
            return jsonify({"success": False, "error": resultado['error']})
            
    except Exception as e:
        logger.error(f"API: Erro ao enviar WhatsApp: {e}")
        return jsonify({"success": False, "error": f"Erro no servidor: {str(e)}"})

# ===== ROTAS DE AUTENTICAÇÃO ADMIN =====

@app.route("/api/admin/login", methods=["POST"])
def api_admin_login():
    """API para login do administrador."""
    try:
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        # Verificação simples (em produção, usar hash e banco de dados)
        if username == 'admin' and password == 'admin123':
            session['admin_logged'] = True
            logger.debug("Admin logado com sucesso")
            return redirect(url_for('admin_dashboard'))
        else:
            logger.warning(f"Tentativa de login inválida: {username}")
            return redirect(url_for('admin_login'))
            
    except Exception as e:
        logger.error(f"Erro no login admin: {e}")
        return redirect(url_for('admin_login'))

@app.route("/api/admin/logout")
def api_admin_logout():
    """API para logout do administrador."""
    session.pop('admin_logged', None)
    logger.debug("Admin deslogado")
    return redirect(url_for('admin_login'))

# ===== CONFIGURAÇÃO DO SERVIDOR =====

if __name__ == "__main__":
    # Usar a porta definida pelo ambiente (Render) ou 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    
    # Escuta em 0.0.0.0 para ser acessível externamente
    app.run(host="0.0.0.0", port=port, debug=False)
