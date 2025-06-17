import requests
import json
import logging
from datetime import datetime
import re

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppSender:
    def __init__(self, api_url=None, api_key=None):
        """
        Inicializa o sender do WhatsApp
        
        Args:
            api_url: URL da API do WhatsApp (Evolution API)
            api_key: Chave da API
        """
        self.api_url = api_url or "https://sua-api-whatsapp.com"
        self.api_key = api_key or "SUA_CHAVE_API"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def limpar_numero_whatsapp(self, numero):
        """
        Limpa e formata o número do WhatsApp
        
        Args:
            numero: Número do WhatsApp (pode ter formatação)
            
        Returns:
            str: Número limpo no formato internacional
        """
        # Remove todos os caracteres não numéricos
        numero_limpo = re.sub(r'[^\d]', '', numero)
        
        # Se não tem código do país, adiciona 55 (Brasil)
        if len(numero_limpo) == 11 and numero_limpo.startswith('11'):
            numero_limpo = '55' + numero_limpo
        elif len(numero_limpo) == 10:
            numero_limpo = '5511' + numero_limpo
        elif len(numero_limpo) == 9:
            numero_limpo = '55119' + numero_limpo
        
        return numero_limpo
    
    def criar_mensagem_sucesso(self, nome_cliente, link_upgrade="https://4nghki1c7l5g.manus.space/upgrade"):
        """
        Cria a mensagem de sucesso personalizada
        
        Args:
            nome_cliente: Nome do cliente
            link_upgrade: Link para a página de upgrade
            
        Returns:
            str: Mensagem formatada
        """
        mensagem = f"""🎉 *Pagamento Confirmado!*

Olá *{nome_cliente}*!

Seu pagamento PIX foi aprovado com sucesso! ✅

🔗 *Acesse sua calculadora completa:*
{link_upgrade}

📱 *Instruções:*
• Clique no link acima
• Siga as instruções para instalar como app
• Aproveite todos os recursos da versão completa!

✨ *Recursos liberados:*
✅ Cálculo para todos os marketplaces
✅ Margem de lucro personalizada  
✅ Histórico de cálculos
✅ Funciona offline
✅ Atualizações automáticas

📞 *Dúvidas?* Responda esta mensagem!

Obrigado pela confiança! 🚀"""
        
        return mensagem
    
    def enviar_mensagem(self, numero_whatsapp, nome_cliente):
        """
        Envia mensagem de sucesso via WhatsApp
        
        Args:
            numero_whatsapp: Número do WhatsApp do cliente
            nome_cliente: Nome do cliente
            
        Returns:
            dict: Resultado do envio
        """
        try:
            # Limpa o número
            numero_limpo = self.limpar_numero_whatsapp(numero_whatsapp)
            
            # Cria a mensagem
            mensagem = self.criar_mensagem_sucesso(nome_cliente)
            
            # Dados para envio
            dados_envio = {
                "number": numero_limpo,
                "message": mensagem
            }
            
            # Faz a requisição para a API
            response = requests.post(
                f"{self.api_url}/message/sendText",
                headers=self.headers,
                json=dados_envio,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"Mensagem enviada com sucesso para {numero_limpo}")
                return {
                    "sucesso": True,
                    "mensagem": "Mensagem enviada com sucesso!",
                    "numero": numero_limpo,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return {
                    "sucesso": False,
                    "erro": f"Erro da API: {response.status_code}",
                    "detalhes": response.text
                }
                
        except requests.exceptions.Timeout:
            logger.error("Timeout ao enviar mensagem")
            return {
                "sucesso": False,
                "erro": "Timeout na requisição",
                "detalhes": "A API demorou muito para responder"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão: {str(e)}")
            return {
                "sucesso": False,
                "erro": "Erro de conexão",
                "detalhes": str(e)
            }
            
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return {
                "sucesso": False,
                "erro": "Erro inesperado",
                "detalhes": str(e)
            }
    
    def testar_conexao(self):
        """
        Testa a conexão com a API do WhatsApp
        
        Returns:
            dict: Resultado do teste
        """
        try:
            response = requests.get(
                f"{self.api_url}/instance/status",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "sucesso": True,
                    "mensagem": "Conexão OK",
                    "status": response.json()
                }
            else:
                return {
                    "sucesso": False,
                    "erro": f"Status: {response.status_code}",
                    "detalhes": response.text
                }
                
        except Exception as e:
            return {
                "sucesso": False,
                "erro": "Erro de conexão",
                "detalhes": str(e)
            }

# Função auxiliar para uso direto
def enviar_link_whatsapp(numero, nome, api_url=None, api_key=None):
    """
    Função auxiliar para enviar link do WhatsApp
    
    Args:
        numero: Número do WhatsApp
        nome: Nome do cliente
        api_url: URL da API (opcional)
        api_key: Chave da API (opcional)
        
    Returns:
        dict: Resultado do envio
    """
    sender = WhatsAppSender(api_url, api_key)
    return sender.enviar_mensagem(numero, nome)

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    sender = WhatsAppSender()
    
    # Teste de limpeza de número
    print("Teste de limpeza de números:")
    numeros_teste = [
        "(11) 99999-8888",
        "11999998888",
        "5511999998888",
        "999998888"
    ]
    
    for num in numeros_teste:
        limpo = sender.limpar_numero_whatsapp(num)
        print(f"{num} -> {limpo}")
    
    # Teste de mensagem
    print("\nTeste de mensagem:")
    mensagem = sender.criar_mensagem_sucesso("João Silva")
    print(mensagem)
