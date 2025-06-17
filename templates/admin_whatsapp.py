from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
from whatsapp_sender import WhatsAppSender, enviar_link_whatsapp

# Template HTML para o painel admin melhorado
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo - PrecificaMKT</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .clients-section {
            padding: 20px;
        }
        
        .section-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .client-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .client-info {
            flex: 1;
        }
        
        .client-name {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .client-details {
            color: #666;
            font-size: 0.9em;
        }
        
        .client-actions {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        
        .btn-whatsapp {
            background: #25D366;
            color: white;
        }
        
        .btn-whatsapp:hover {
            background: #128C7E;
        }
        
        .btn-whatsapp:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .btn-edit {
            background: #ffc107;
            color: #333;
        }
        
        .btn-edit:hover {
            background: #e0a800;
        }
        
        .btn-delete {
            background: #dc3545;
            color: white;
        }
        
        .btn-delete:hover {
            background: #c82333;
        }
        
        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-sent {
            background: #d4edda;
            color: #155724;
        }
        
        .alert {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            display: none;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .config-section {
            padding: 20px;
            border-top: 1px solid #dee2e6;
            background: #f8f9fa;
        }
        
        .config-form {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-group label {
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        .form-group input {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }
        
        @media (max-width: 768px) {
            .client-card {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .client-actions {
                margin-top: 10px;
                width: 100%;
                justify-content: flex-end;
            }
            
            .config-form {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Painel Administrativo</h1>
            <p>Sistema de Precipício de Preços - PrecificaMKT</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_clientes }}</div>
                <div>Total de Clientes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ links_enviados }}</div>
                <div>Links Enviados</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ pendentes }}</div>
                <div>Pendentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">R$ {{ receita_total }}</div>
                <div>Receita Total</div>
            </div>
        </div>
        
        <div class="clients-section">
            <h2 class="section-title">📋 Clientes Cadastrados</h2>
            
            <div id="alert-container"></div>
            
            {% for cliente in clientes %}
            <div class="client-card">
                <div class="client-info">
                    <div class="client-name">{{ cliente.nome }}</div>
                    <div class="client-details">
                        📧 {{ cliente.email }}<br>
                        📱 {{ cliente.whatsapp }}<br>
                        🕒 {{ cliente.data_cadastro }}
                        <span class="status-badge status-{{ cliente.status }}">
                            {{ 'Link Enviado' if cliente.status == 'sent' else 'Pendente' }}
                        </span>
                    </div>
                </div>
                <div class="client-actions">
                    <button class="btn btn-whatsapp" 
                            onclick="enviarWhatsApp('{{ cliente.whatsapp }}', '{{ cliente.nome }}', '{{ cliente.id }}')"
                            {{ 'disabled' if cliente.status == 'sent' else '' }}>
                        📱 {{ 'Reenviado' if cliente.status == 'sent' else 'Enviar Link' }}
                    </button>
                    <button class="btn btn-edit" onclick="editarCliente('{{ cliente.id }}')">
                        ✏️ Editar
                    </button>
                    <button class="btn btn-delete" onclick="excluirCliente('{{ cliente.id }}')">
                        🗑️ Excluir
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="config-section">
            <h2 class="section-title">⚙️ Configurações do WhatsApp</h2>
            <form class="config-form" onsubmit="salvarConfig(event)">
                <div class="form-group">
                    <label for="api_url">URL da API WhatsApp:</label>
                    <input type="url" id="api_url" name="api_url" 
                           value="{{ config.api_url or 'https://sua-api-whatsapp.com' }}"
                           placeholder="https://sua-api-whatsapp.com">
                </div>
                <div class="form-group">
                    <label for="api_key">Chave da API:</label>
                    <input type="text" id="api_key" name="api_key" 
                           value="{{ config.api_key or 'SUA_CHAVE_API' }}"
                           placeholder="SUA_CHAVE_API">
                </div>
                <div class="form-group">
                    <button type="submit" class="btn btn-whatsapp">💾 Salvar Configurações</button>
                </div>
                <div class="form-group">
                    <button type="button" class="btn btn-edit" onclick="testarConexao()">🔍 Testar Conexão</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        function mostrarAlerta(mensagem, tipo) {
            const container = document.getElementById('alert-container');
            const alert = document.createElement('div');
            alert.className = `alert alert-${tipo}`;
            alert.textContent = mensagem;
            alert.style.display = 'block';
            
            container.innerHTML = '';
            container.appendChild(alert);
            
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
        
        async function enviarWhatsApp(whatsapp, nome, clienteId) {
            const btn = event.target;
            const textoOriginal = btn.textContent;
            
            btn.disabled = true;
            btn.textContent = '📤 Enviando...';
            
            try {
                const response = await fetch('/enviar-whatsapp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        whatsapp: whatsapp,
                        nome: nome,
                        cliente_id: clienteId
                    })
                });
                
                const result = await response.json();
                
                if (result.sucesso) {
                    mostrarAlerta('✅ Link enviado com sucesso!', 'success');
                    btn.textContent = '✅ Enviado';
                    btn.style.background = '#28a745';
                    
                    // Atualizar status na interface
                    const statusBadge = btn.closest('.client-card').querySelector('.status-badge');
                    statusBadge.textContent = 'Link Enviado';
                    statusBadge.className = 'status-badge status-sent';
                } else {
                    mostrarAlerta(`❌ Erro: ${result.erro}`, 'error');
                    btn.disabled = false;
                    btn.textContent = textoOriginal;
                }
            } catch (error) {
                mostrarAlerta(`❌ Erro de conexão: ${error.message}`, 'error');
                btn.disabled = false;
                btn.textContent = textoOriginal;
            }
        }
        
        async function salvarConfig(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const config = {
                api_url: formData.get('api_url'),
                api_key: formData.get('api_key')
            };
            
            try {
                const response = await fetch('/salvar-config', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(config)
                });
                
                const result = await response.json();
                
                if (result.sucesso) {
                    mostrarAlerta('✅ Configurações salvas com sucesso!', 'success');
                } else {
                    mostrarAlerta(`❌ Erro: ${result.erro}`, 'error');
                }
            } catch (error) {
                mostrarAlerta(`❌ Erro: ${error.message}`, 'error');
            }
        }
        
        async function testarConexao() {
            const btn = event.target;
            const textoOriginal = btn.textContent;
            
            btn.disabled = true;
            btn.textContent = '🔍 Testando...';
            
            try {
                const response = await fetch('/testar-whatsapp');
                const result = await response.json();
                
                if (result.sucesso) {
                    mostrarAlerta('✅ Conexão OK! WhatsApp funcionando.', 'success');
                } else {
                    mostrarAlerta(`❌ Erro na conexão: ${result.erro}`, 'error');
                }
            } catch (error) {
                mostrarAlerta(`❌ Erro: ${error.message}`, 'error');
            } finally {
                btn.disabled = false;
                btn.textContent = textoOriginal;
            }
        }
        
        function editarCliente(clienteId) {
            // Implementar edição de cliente
            mostrarAlerta('🔧 Função de edição em desenvolvimento', 'success');
        }
        
        function excluirCliente(clienteId) {
            if (confirm('Tem certeza que deseja excluir este cliente?')) {
                // Implementar exclusão
                mostrarAlerta('🗑️ Função de exclusão em desenvolvimento', 'success');
            }
        }
    </script>
</body>
</html>
"""

def carregar_clientes():
    """Carrega a lista de clientes do arquivo JSON"""
    try:
        if os.path.exists('cadastros.json'):
            with open('cadastros.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Erro ao carregar clientes: {e}")
        return []

def salvar_clientes(clientes):
    """Salva a lista de clientes no arquivo JSON"""
    try:
        with open('cadastros.json', 'w', encoding='utf-8') as f:
            json.dump(clientes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar clientes: {e}")
        return False

def carregar_config():
    """Carrega configurações do WhatsApp"""
    try:
        if os.path.exists('whatsapp_config.json'):
            with open('whatsapp_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"api_url": "", "api_key": ""}
    except Exception as e:
        print(f"Erro ao carregar config: {e}")
        return {"api_url": "", "api_key": ""}

def salvar_config(config):
    """Salva configurações do WhatsApp"""
    try:
        with open('whatsapp_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar config: {e}")
        return False

# Rotas para integração com o sistema principal
def criar_rotas_whatsapp(app):
    """Cria as rotas do WhatsApp no app Flask principal"""
    
    @app.route('/admin-whatsapp')
    def admin_whatsapp():
        """Página do painel administrativo com WhatsApp"""
        clientes = carregar_clientes()
        config = carregar_config()
        
        # Calcular estatísticas
        total_clientes = len(clientes)
        links_enviados = len([c for c in clientes if c.get('status') == 'sent'])
        pendentes = total_clientes - links_enviados
        receita_total = total_clientes * 15.99  # R$ 15,99 por cliente
        
        # Formatar dados dos clientes
        for cliente in clientes:
            if 'status' not in cliente:
                cliente['status'] = 'pending'
            if 'data_cadastro' not in cliente:
                cliente['data_cadastro'] = 'Data não informada'
        
        return render_template_string(ADMIN_TEMPLATE, 
                                    clientes=clientes,
                                    config=config,
                                    total_clientes=total_clientes,
                                    links_enviados=links_enviados,
                                    pendentes=pendentes,
                                    receita_total=f"{receita_total:.2f}")
    
    @app.route('/enviar-whatsapp', methods=['POST'])
    def enviar_whatsapp_route():
        """Rota para enviar WhatsApp"""
        try:
            dados = request.get_json()
            whatsapp = dados.get('whatsapp')
            nome = dados.get('nome')
            cliente_id = dados.get('cliente_id')
            
            if not whatsapp or not nome:
                return jsonify({
                    "sucesso": False,
                    "erro": "WhatsApp e nome são obrigatórios"
                })
            
            # Carregar configurações
            config = carregar_config()
            
            # Enviar mensagem
            resultado = enviar_link_whatsapp(
                whatsapp, 
                nome, 
                config.get('api_url'), 
                config.get('api_key')
            )
            
            # Atualizar status do cliente se enviado com sucesso
            if resultado.get('sucesso'):
                clientes = carregar_clientes()
                for cliente in clientes:
                    if cliente.get('id') == cliente_id or cliente.get('whatsapp') == whatsapp:
                        cliente['status'] = 'sent'
                        cliente['data_envio'] = datetime.now().isoformat()
                        break
                salvar_clientes(clientes)
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                "sucesso": False,
                "erro": "Erro interno",
                "detalhes": str(e)
            })
    
    @app.route('/salvar-config', methods=['POST'])
    def salvar_config_route():
        """Rota para salvar configurações"""
        try:
            config = request.get_json()
            
            if salvar_config(config):
                return jsonify({"sucesso": True})
            else:
                return jsonify({
                    "sucesso": False,
                    "erro": "Erro ao salvar configurações"
                })
                
        except Exception as e:
            return jsonify({
                "sucesso": False,
                "erro": str(e)
            })
    
    @app.route('/testar-whatsapp')
    def testar_whatsapp_route():
        """Rota para testar conexão WhatsApp"""
        try:
            config = carregar_config()
            sender = WhatsAppSender(config.get('api_url'), config.get('api_key'))
            resultado = sender.testar_conexao()
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                "sucesso": False,
                "erro": str(e)
            })

# Exemplo de uso
if __name__ == "__main__":
    from flask import Flask
    
    app = Flask(__name__)
    criar_rotas_whatsapp(app)
    
    @app.route('/')
    def home():
        return '<a href="/admin-whatsapp">Ir para Painel Admin WhatsApp</a>'
    
    app.run(debug=True, host='0.0.0.0', port=5000)
