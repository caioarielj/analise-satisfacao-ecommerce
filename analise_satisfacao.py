# ============================================
# ANÁLISE DE SATISFAÇÃO DO CLIENTE - E-COMMERCE
# ============================================

# Objetivo:
# Identificar quais fatores impactam a satisfação do cliente,
# com foco em atraso, tempo de entrega e frete.

# ============================================
# 1. IMPORTS
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# ============================================
# 2. CARREGAMENTO DOS DADOS
# ============================================

data_path = 'data/'

pedidos = pd.read_csv(data_path + 'pedidos.csv')
comentarios = pd.read_csv(data_path + 'comentarios.csv')
itens = pd.read_csv(data_path + 'itens_do_pedido.csv')

# ============================================
# 3. TRATAMENTO DOS DADOS
# ============================================

# Filtrar pedidos entregues
pedidos_entregues = pedidos[pedidos['status_pedido'] == 'delivered'].copy()

# Converter datas
pedidos_entregues['data_entrega_cliente_pedido'] = pd.to_datetime(
    pedidos_entregues['data_entrega_cliente_pedido'], errors='coerce'
)

pedidos_entregues['data_entrega_estimada_pedido'] = pd.to_datetime(
    pedidos_entregues['data_entrega_estimada_pedido'], errors='coerce'
)

# Remover nulos
pedidos_entregues = pedidos_entregues[
    pedidos_entregues['data_entrega_cliente_pedido'].notna()
]

# Criar status de entrega
pedidos_entregues['status_entrega'] = (
    pedidos_entregues['data_entrega_cliente_pedido'] >
    pedidos_entregues['data_entrega_estimada_pedido']
).map({True: 'atrasado', False: 'no prazo'})

# Merge com avaliações
df = pedidos_entregues.merge(
    comentarios[['id_pedido', 'nota_avaliacao']],
    on='id_pedido',
    how='inner'
)

# ============================================
# 4. ANÁLISE 1 — IMPACTO DO ATRASO
# ============================================

print("\n=== ANÁLISE: ATRASO ===")

# Taxa de satisfação (nota >= 4)
df['satisfeito'] = (df['nota_avaliacao'] >= 4).astype(int)

taxa_satisfacao = df.groupby('status_entrega')['satisfeito'].mean()
print("\nTaxa de satisfação:")
print(taxa_satisfacao)

# Teste estatístico
grupo_atrasado = df[df['status_entrega'] == 'atrasado']['nota_avaliacao']
grupo_prazo = df[df['status_entrega'] == 'no prazo']['nota_avaliacao']

teste = ttest_ind(grupo_atrasado, grupo_prazo, equal_var=False)
print("\nTeste T:", teste)

# Gráfico
sns.countplot(
    data=df,
    x='nota_avaliacao',
    hue='status_entrega',
    hue_order=['atrasado', 'no prazo']
)

plt.title('Distribuição das Avaliações por Status de Entrega')
plt.xlabel('Nota de Avaliação')
plt.ylabel('Quantidade de Pedidos')
plt.show()

# ============================================
# 5. ANÁLISE 2 — TEMPO DE ENTREGA
# ============================================

print("\n=== ANÁLISE: TEMPO DE ENTREGA ===")

df['timestamp_compra_pedido'] = pd.to_datetime(
    df['timestamp_compra_pedido'], errors='coerce'
)

df['tempo_entrega_dias'] = (
    df['data_entrega_cliente_pedido'] -
    df['timestamp_compra_pedido']
).dt.days

# Criar faixas
df['faixa_tempo'] = pd.cut(
    df['tempo_entrega_dias'],
    bins=[0, 3, 7, 14, 30, 100],
    labels=['0-3', '4-7', '8-14', '15-30', '30+']
)

tempo_media = df.groupby('faixa_tempo')['nota_avaliacao'].mean()
print("\nNota média por tempo de entrega:")
print(tempo_media)

# Gráfico
tempo_media.plot(marker='o')
plt.title('Nota Média por Tempo de Entrega')
plt.xlabel('Faixa de Tempo (dias)')
plt.ylabel('Nota Média')
plt.grid()
plt.show()

# ============================================
# 6. ANÁLISE 3 — FRETE
# ============================================

print("\n=== ANÁLISE: FRETE ===")

frete_por_pedido = itens.groupby('id_pedido')['valor_frete'].sum().reset_index()

df = df.merge(frete_por_pedido, on='id_pedido', how='left')

# Criar faixas de frete
df['faixa_frete'] = pd.cut(
    df['valor_frete'],
    bins=[0, 10, 20, 50, 100, 1000],
    labels=['0-10', '10-20', '20-50', '50-100', '100+']
)

frete_media = df.groupby('faixa_frete')['nota_avaliacao'].mean()
print("\nNota média por faixa de frete:")
print(frete_media)

# Gráfico
frete_media.plot(marker='o')
plt.title('Nota Média por Faixa de Frete')
plt.xlabel('Faixa de Frete')
plt.ylabel('Nota Média')
plt.grid()
plt.show()

# ============================================
# 7. CONCLUSÃO
# ============================================

print("\n=== CONCLUSÃO ===")

print("""
O cumprimento do prazo é o principal fator de satisfação do cliente.

Pedidos no prazo apresentam taxa de satisfação significativamente maior
do que pedidos atrasados.

O tempo de entrega também impacta negativamente a experiência, especialmente
em prazos mais longos.

O valor do frete possui impacto menor em comparação aos fatores logísticos.

Recomenda-se priorizar a redução de atrasos e a melhoria da eficiência logística.
""")