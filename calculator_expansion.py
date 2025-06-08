import math

def calculate_magalu_price(cost_price, profit_margin, category_type="geral", additional_options=None):
    """
    Calcula o preço de venda para o Magazine Luiza com base no custo, margem de lucro e categoria.
    
    Args:
        cost_price (float): Preço de custo do produto em R$
        profit_margin (float): Margem de lucro desejada em porcentagem (ex: 30 para 30%)
        category_type (str): Categoria do produto (geral, eletronicos, moda, casa)
        additional_options (dict): Opções adicionais (não utilizado no momento)
        
    Returns:
        float: Preço de venda sugerido em R$
    """
    # Validação de entrada
    if cost_price <= 0:
        raise ValueError("O preço de custo deve ser maior que zero")
    if profit_margin < 0:
        raise ValueError("A margem de lucro não pode ser negativa")
    
    # Define a taxa de comissão com base na categoria
    if category_type.lower() in ["eletronicos", "informatica", "celulares", "smartphones"]:
        commission_rate = 0.14  # 14% para eletrônicos, informática, celulares
    elif category_type.lower() in ["moda", "acessorios", "beleza", "perfumaria"]:
        commission_rate = 0.20  # 20% para moda, acessórios, beleza
    elif category_type.lower() in ["casa", "decoracao", "moveis"]:
        commission_rate = 0.18  # 18% para casa e decoração
    else:
        commission_rate = 0.16  # 16% taxa média para outras categorias
    
    # Cálculo do preço de venda
    # Fórmula: preço_venda = (custo + (custo * margem_lucro/100)) / (1 - taxa_comissao)
    profit_factor = profit_margin / 100
    price_with_profit = cost_price * (1 + profit_factor)
    final_price = price_with_profit / (1 - commission_rate)
    
    # Arredonda para duas casas decimais
    final_price = math.ceil(final_price * 100) / 100
    
    return final_price

def calculate_americanas_price(cost_price, profit_margin, category_type="geral", additional_options=None):
    """
    Calcula o preço de venda para Lojas Americanas com base no custo, margem de lucro e categoria.
    
    Args:
        cost_price (float): Preço de custo do produto em R$
        profit_margin (float): Margem de lucro desejada em porcentagem (ex: 30 para 30%)
        category_type (str): Categoria do produto (telefonia, moveis, higiene, moda)
        additional_options (dict): Opções adicionais (não utilizado no momento)
        
    Returns:
        float: Preço de venda sugerido em R$
    """
    # Validação de entrada
    if cost_price <= 0:
        raise ValueError("O preço de custo deve ser maior que zero")
    if profit_margin < 0:
        raise ValueError("A margem de lucro não pode ser negativa")
    
    # Define a taxa de comissão com base na categoria
    if category_type.lower() in ["telefonia", "eletronicos", "eletrodomesticos", "informatica"]:
        commission_rate = 0.16  # 16% para telefonia, eletrônicos, eletrodomésticos
    elif category_type.lower() in ["moveis", "utilidades", "papelaria", "importacao"]:
        commission_rate = 0.165  # 16.5% para móveis, utilidades, papelaria
    elif category_type.lower() in ["higiene", "beleza", "suplementos", "livros", "esporte"]:
        commission_rate = 0.17  # 17% para higiene, beleza, suplementos
    elif category_type.lower() in ["moda", "calcados", "acessorios"]:
        commission_rate = 0.19  # 19% para moda, calçados, acessórios
    else:
        commission_rate = 0.17  # 17% taxa média para outras categorias
    
    # Cálculo do preço de venda
    # Fórmula: preço_venda = (custo + (custo * margem_lucro/100)) / (1 - taxa_comissao)
    profit_factor = profit_margin / 100
    price_with_profit = cost_price * (1 + profit_factor)
    final_price = price_with_profit / (1 - commission_rate)
    
    # Arredonda para duas casas decimais
    final_price = math.ceil(final_price * 100) / 100
    
    return final_price
