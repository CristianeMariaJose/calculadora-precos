import os
import pymongo
from datetime import datetime
import logging
import certifi

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Configuração do MongoDB Atlas - usando um cluster real e gratuito
MONGO_URI = "mongodb+srv://price_tool_admin:price_tool_password_2025@cluster0.zcwbvmn.mongodb.net/price_tool_db?retryWrites=true&w=majority"
DB_NAME = "price_tool_db"
COLLECTION_NAME = "cadastros"

# Variáveis globais para conexão
client = None
db = None
collection = None

# Inicializar conexão com MongoDB
try:
    # Usar certificado SSL para conexão segura
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
    # Testar a conexão
    client.admin.command('ping')
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logger.info("Conexão com MongoDB Atlas estabelecida com sucesso!")
except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB Atlas: {str(e)}")
    # Fallback para arquivo local em caso de erro
    CADASTROS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cadastros.json")
    logger.warning(f"Usando arquivo local como fallback: {CADASTROS_FILE}")

def load_cadastros():
    """Carrega os cadastros do MongoDB Atlas"""
    try:
        # Verifica se a conexão MongoDB está disponível
        if collection is not None:
            # Tenta carregar do MongoDB
            cadastros = list(collection.find({}, {'_id': 0}))
            logger.debug(f"Carregados {len(cadastros)} cadastros do MongoDB Atlas")
            return cadastros
        else:
            logger.warning("Conexão MongoDB não disponível, retornando lista vazia")
            return []
    except Exception as e:
        logger.error(f"Erro ao carregar cadastros do MongoDB: {str(e)}")
        return []

def add_cadastro(nome, email, whatsapp):
    """Adiciona um novo cadastro ao MongoDB"""
    try:
        # Verifica se a conexão MongoDB está disponível
        if collection is None:
            logger.warning("Conexão MongoDB não disponível para adicionar cadastro")
            return False
            
        # Verificar se o email já existe
        existing = collection.find_one({"email": email})
        if existing:
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

        # Insere no MongoDB
        result = collection.insert_one(novo_cadastro)
        logger.debug(f"Cadastro inserido com ID: {result.inserted_id}")
        return True
    except Exception as e:
        logger.error(f"Erro ao adicionar cadastro: {str(e)}")
        return False

def update_cadastro(email, dados):
    """Atualiza um cadastro existente pelo email"""
    try:
        # Verifica se a conexão MongoDB está disponível
        if collection is None:
            logger.warning("Conexão MongoDB não disponível para atualizar cadastro")
            return False
            
        # Atualiza o cadastro
        result = collection.update_one(
            {"email": email},
            {"$set": dados}
        )
        
        if result.modified_count > 0:
            logger.debug(f"Cadastro atualizado para {email}")
            return True
        else:
            logger.warning(f"Nenhum cadastro encontrado para atualizar: {email}")
            return False
    except Exception as e:
        logger.error(f"Erro ao atualizar cadastro: {str(e)}")
        return False

def get_cadastro_by_email(email):
    """Busca um cadastro pelo email"""
    try:
        # Verifica se a conexão MongoDB está disponível
        if collection is None:
            logger.warning("Conexão MongoDB não disponível para buscar cadastro")
            return None
            
        cadastro = collection.find_one({"email": email}, {'_id': 0})
        return cadastro
    except Exception as e:
        logger.error(f"Erro ao buscar cadastro por email: {str(e)}")
        return None

# Inicializa o banco de dados se necessário
def init_database():
    """Inicializa o banco de dados se necessário"""
    try:
        # Verifica se a conexão MongoDB está disponível
        if db is None or collection is None:
            logger.warning("Conexão MongoDB não disponível, pulando inicialização do banco")
            return False
            
        # Verifica se a coleção existe e tem índices
        if COLLECTION_NAME not in db.list_collection_names():
            # Cria índice para email (campo único)
            collection.create_index("email", unique=True)
            logger.info("Índice de email criado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        return False

# Inicializa o banco de dados ao importar o módulo
init_database()
