# Documentação: Calculadora e Monitor de Preços para Marketplaces

## Visão Geral

Esta aplicação web permite que vendedores de marketplaces calculem preços ideais para seus produtos considerando as diferentes taxas de cada plataforma, além de monitorar os preços ao longo do tempo.

## Funcionalidades Principais

1. **Calculadora de Preços**
   - Cálculo personalizado para Mercado Livre, Amazon, Shopee, Magazine Luiza e Lojas Americanas
   - Considera taxas específicas de cada marketplace
   - Ajusta automaticamente para diferentes tipos de anúncio e programas

2. **Monitor de Preços**
   - Acompanhamento de preços em diferentes marketplaces
   - Adição de novos produtos para monitoramento
   - Atualização de preços em tempo real

## Como Usar

### Calculadora de Preços

1. Acesse a página inicial da aplicação
2. Preencha os campos:
   - **Custo do Produto**: O valor que você paga pelo produto (R$)
   - **Margem de Lucro Desejada**: Sua margem de lucro alvo (%)
   - **Marketplace**: Selecione entre Mercado Livre, Amazon, Shopee, Magazine Luiza ou Lojas Americanas
   - **Categoria do Produto**: Para Magazine Luiza e Americanas, selecione a categoria específica
   - **Taxa da Categoria**: A taxa específica da categoria do seu produto (%)
   
3. Opções específicas por marketplace:
   - **Mercado Livre**: Escolha entre anúncio Clássico ou Premium
   - **Shopee**: Indique se participa do Programa de Frete Grátis
   - **Magazine Luiza**: Selecione a categoria do produto
   - **Lojas Americanas**: Selecione a categoria do produto

4. Clique em "Calcular Preço" para obter o preço de venda sugerido

### Monitor de Preços

1. Clique no link "Ver Monitor de Preços" na página inicial
2. Visualize os preços atuais dos produtos já cadastrados
3. Para adicionar um novo produto:
   - Preencha o nome do produto
   - Adicione os IDs/SKUs do produto em cada marketplace relevante (incluindo Magazine Luiza e Americanas)
   - Clique em "Adicionar Produto"
4. Use o botão "Atualizar Preços" para obter os valores mais recentes

## Taxas de Marketplaces (Maio 2025)

### Mercado Livre

- **Anúncio Clássico**:
  - Tarifa: 10% a 14% (varia por categoria)
  - Custo fixo: R$ 6,25 (produtos < R$ 29), R$ 6,50 (R$ 29-50), R$ 6,75 (R$ 50-79), R$ 0 (> R$ 79)
  - Sem parcelamento sem juros

- **Anúncio Premium**:
  - Tarifa: 15% a 19% (varia por categoria)
  - Mesmos custos fixos do Clássico
  - Até 12x sem juros (depende do valor e meio de pagamento)

### Amazon Brasil

- Comissão: 9% a 15% (varia por categoria)
- Exemplo Móveis: 15% sobre primeiros R$ 200, 10% sobre excedente
- Planos disponíveis:
  - Individual: Sem mensalidade, taxa por item vendido
  - Profissional: Mensalidade (R$ 19/mês), sem taxa por item

### Shopee Brasil

- Comissão padrão: 14% (13% + 1% transação) + R$ 4,00 por item
- Com Programa Frete Grátis: 20% (14% + 6%) + R$ 4,00 por item
- Regras específicas para vendedores CPF vs CNPJ

### Magazine Luiza (Magalu)

- **Comissões por Categoria**:
  - Eletrônicos, Informática, Celulares: 10-14%
  - Moda, Acessórios, Beleza: 16-20%
  - Casa e Decoração: 14-18%
  - Média geral: 16%

- **Taxas Adicionais**:
  - Não há taxa de adesão ou mensalidade
  - Frete: O Magalu oferece serviço de logística (Magalu Entregas) sem custos adicionais para o lojista

- **Fonte**: Nuvemshop Blog (Maio 2025), Universo Magalu

### Lojas Americanas

- **Comissões por Categoria**:
  - Telefonia, Eletrônicos, Eletrodomésticos: 16%
  - Móveis, Utilidades, Papelaria, Importação: 16,5%
  - Higiene, Beleza, Suplementos, Livros, Esporte: 17%
  - Moda, Calçados, Acessórios: 19%

- **Taxas Adicionais**:
  - Não há taxa de adesão ou mensalidade
  - Comissão é calculada sobre o valor total da venda

- **Fonte**: Americanas Marketplace (Maio 2025)

## Requisitos Técnicos

- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexão com internet

## Limitações Atuais

- Integração real com APIs da Amazon, Shopee, Magazine Luiza e Americanas requer credenciais e configuração adicional
- Monitoramento de preços usa valores simulados para Amazon, Shopee, Magazine Luiza e Americanas
- Dados não são persistidos entre sessões (reiniciar o servidor limpa os produtos adicionados)

## Próximos Passos

Para uma versão completa em produção, seria necessário:

1. Implementar autenticação de usuários
2. Adicionar banco de dados para persistência
3. Configurar credenciais reais para todas as APIs
4. Implementar notificações de mudanças de preço
5. Adicionar mais marketplaces (Casas Bahia, Submarino, etc.)
