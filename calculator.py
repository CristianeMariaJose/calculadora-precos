import math

def calculate_mercado_livre_price(cost_price, profit_margin, listing_type="classico", category_fee=None):
    """
    Calcula o preço de venda para o Mercado Livre com base no custo, margem de lucro e tipo de anúncio.
    
    Args:
        cost_price (float): Preço de custo do produto em R$
        profit_margin (float): Margem de lucro desejada em porcentagem (ex: 30 para 30%)
        listing_type (str): Tipo de anúncio no Mercado Livre ("classico" ou "premium")
        category_fee (float): Taxa específica da categoria em porcentagem (opcional)
        
    Returns:
        float: Preço de venda sugerido em R$
    """
    # Validação de entrada
    if cost_price <= 0:
        raise ValueError("O preço de custo deve ser maior que zero")
    if profit_margin < 0:
        raise ValueError("A margem de lucro não pode ser negativa")
    
    # Define a taxa de comissão com base no tipo de anúncio e categoria
    if listing_type.lower() == "premium":
        if category_fee is not None:
            commission_rate = category_fee / 100
        else:
            commission_rate = 0.17  # 17% taxa média para anúncios premium
    else:  # Clássico
        if category_fee is not None:
            commission_rate = category_fee / 100
        else:
            commission_rate = 0.12  # 12% taxa média para anúncios clássicos
    
    # Cálculo do preço de venda
    # Fórmula: preço_venda = (custo + (custo * margem_lucro/100)) / (1 - taxa_comissao)
    profit_factor = profit_margin / 100
    price_with_profit = cost_price * (1 + profit_factor)
    final_price = price_with_profit / (1 - commission_rate)
    
    # Adiciona taxa fixa para produtos abaixo de R$ 79
    if final_price < 29:
        final_price += 6.25
    elif final_price < 50:
        final_price += 6.50
    elif final_price < 79:
        final_price += 6.75
    
    # Arredonda para duas casas decimais
    final_price = math.ceil(final_price * 100) / 100
    
    return final_price

def calculate_amazon_price(cost_price, profit_margin, category_fee=None, selling_plan="professional"):
    """
    Calcula o preço de venda para a Amazon com base no custo, margem de lucro e plano de vendas.
    
    Args:
        cost_price (float): Preço de custo do produto em R$
        profit_margin (float): Margem de lucro desejada em porcentagem (ex: 30 para 30%)
        category_fee (float): Taxa específica da categoria em porcentagem (opcional)
        selling_plan (str): Plano de vendas na Amazon ("professional" ou "individual")
        
    Returns:
        float: Preço de venda sugerido em R$
    """
    # Validação de entrada
    if cost_price <= 0:
        raise ValueError("O preço de custo deve ser maior que zero")
    if profit_margin < 0:
        raise ValueError("A margem de lucro não pode ser negativa")
    
    # Define a taxa de comissão com base na categoria
    if category_fee is not None:
        commission_rate = category_fee / 100
    else:
        commission_rate = 0.15  # 15% taxa média para produtos na Amazon
    
    # Cálculo do preço de venda
    # Fórmula: preço_venda = (custo + (custo * margem_lucro/100)) / (1 - taxa_comissao)
    profit_factor = profit_margin / 100
    price_with_profit = cost_price * (1 + profit_factor)
    
    # Adiciona taxa fixa para plano individual (R$ 1,99 por item)
    if selling_plan.lower() == "individual":
        price_with_profit += 1.99
    
    final_price = price_with_profit / (1 - commission_rate)
    
    # Arredonda para duas casas decimais
    final_price = math.ceil(final_price * 100) / 100
    
    return final_price

def calculate_shopee_price(cost_price, profit_margin, frete_gratis_program=False):
    """
    Calcula o preço de venda para a Shopee com base no custo, margem de lucro e participação no programa de frete grátis.
    
    Args:
        cost_price (float): Preço de custo do produto em R$
        profit_margin (float): Margem de lucro desejada em porcentagem (ex: 30 para 30%)
        frete_gratis_program (bool): Se participa do programa de frete grátis da Shopee
        
    Returns:
        float: Preço de venda sugerido em R$
    """
    # Validação de entrada
    if cost_price <= 0:
        raise ValueError("O preço de custo deve ser maior que zero")
    if profit_margin < 0:
        raise ValueError("A margem de lucro não pode ser negativa")
    
    # Define a taxa de comissão com base na participação no programa de frete grátis
    if frete_gratis_program:
        commission_rate = 0.20  # 20% para participantes do programa de frete grátis
    else:
        commission_rate = 0.14  # 14% taxa padrão (13% comissão + 1% transação)
    
    # Cálculo do preço de venda
    # Fórmula: preço_venda = (custo + (custo * margem_lucro/100) + taxa_fixa) / (1 - taxa_comissao)
    profit_factor = profit_margin / 100
    price_with_profit = cost_price * (1 + profit_factor)
    
    # Adiciona taxa fixa de R$ 4,00 por item
    price_with_profit += 4.00
    
    final_price = price_with_profit / (1 - commission_rate)
    
    # Arredonda para duas casas decimais
    final_price = math.ceil(final_price * 100) / 100
    
    return final_price
