import os
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Arquivo para armazenar os cadastros (em produção seria um banco de dados)
CADASTROS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cadastros.json")

def load_cadastros():
    """Carrega os cadastros do arquivo JSON"""
    try:
        if os.path.exists(CADASTROS_FILE):
            with open(CADASTROS_FILE, 'r') as f:
                logger.debug(f"Carregando cadastros de {CADASTROS_FILE}")
                return json.load(f)
        else:
            logger.debug(f"Arquivo {CADASTROS_FILE} não existe, retornando lista vazia")
            return []
    except Exception as e:
        logger.error(f"Erro ao carregar cadastros: {e}")
        return []

def save_cadastros(cadastros):
    """Salva os cadastros no arquivo JSON"""
    try:
        with open(CADASTROS_FILE, 'w') as f:
            logger.debug(f"Salvando {len(cadastros)} cadastros em {CADASTROS_FILE}")
            json.dump(cadastros, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar cadastros: {e}")
        return False

def add_cadastro(nome, email, whatsapp):
    """Adiciona um novo cadastro"""
    cadastros = load_cadastros()
    
    # Verificar se o email já existe
    for cadastro in cadastros:
        if cadastro.get("email") == email:
            logger.warning(f"Email já cadastrado: {email}")
            return False
    
    # Cria o novo cadastro
    novo_cadastro = {
        "nome": nome,
        "email": email,
        "whatsapp": whatsapp,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pagamento_confirmado": False,
        "licenca_enviada": False
    }
    
    # Adiciona à lista
    cadastros.append(novo_cadastro)
    
    # Salva no arquivo
    return save_cadastros(cadastros)

def update_cadastro(email, dados):
    """Atualiza um cadastro existente pelo email"""
    cadastros = load_cadastros()
    
    for i, cadastro in enumerate(cadastros):
        if cadastro.get("email") == email:
            # Atualiza os campos fornecidos
            for key, value in dados.items():
                cadastros[i][key] = value
            
            # Salva as alterações
            return save_cadastros(cadastros)
    
    logger.warning(f"Cadastro não encontrado para atualizar: {email}")
    return False

def get_cadastro_by_email(email):
    """Busca um cadastro pelo email"""
    cadastros = load_cadastros()
    
    for cadastro in cadastros:
        if cadastro.get("email") == email:
            return cadastro
    
    return None

# Inicializa o arquivo se não existir
if not os.path.exists(CADASTROS_FILE):
    with open(CADASTROS_FILE, 'w') as f:
        json.dump([], f)
    logger.info(f"Arquivo de cadastros criado em {CADASTROS_FILE}")
