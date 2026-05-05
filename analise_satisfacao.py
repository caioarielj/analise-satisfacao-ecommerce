# ============================================
# ANÁLISE DE SATISFAÇÃO DO CLIENTE - E-COMMERCE
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# ============================================
# 1. CARREGAMENTO DOS DADOS
# ============================================

data_path = ''

pedidos = pd.read_csv(data_path + 'pedidos.csv')
comentarios = pd.read_csv(data_path + 'comentarios.csv')
itens = pd.read_csv(data_path + 'itens_do_pedido.csv')

# ============================================
# 2. TRADUÇÃO DAS COLUNAS
# ============================================

columns_translation = {
    'order_id': 'id_pedido',
    'order_status': 'status_pedido',
    'order_purchase_timestamp': 'timestamp_compra_pedido',
    'order_delivered_customer_date': 'data_entrega_cliente_pedido',
    'order_estimated_delivery_date': 'data_entrega_estimada_pedido',
    'review_score': 'nota_avaliacao',
    'freight_value': 'valor_frete'
}

pedidos.rename(columns=columns_translation, inplace=True)
comentarios.rename(columns=columns_translation, inplace=True)
itens.rename(columns=columns_translation, inplace=True)

# ============================================
# 3. TRATAMENTO DOS DADOS
# ============================================

pedidos_entregues = pedidos[pedidos['status_pedido'] == 'delivered'].copy()

pedidos_entregues['data_entrega_cliente_pedido'] = pd.to_datetime(
    pedidos_entregues['data_entrega_cliente_pedido'], errors='coerce'
)

pedidos_entregues['data_entrega_estimada_pedido'] = pd.to_datetime(
    pedidos_entregues['data_entrega_estimada_pedido'], errors='coerce'
)

pedidos_entregues = pedidos_entregues[
    pedidos_entregues['data_entrega_cliente_pedido'].notna()
]

pedidos_entregues['status entrega'] = (
    pedidos_entregues['data_entrega_cliente_pedido'] >
    pedidos_entregues['data_entrega_estimada_pedido']
).map({True: 'atrasado', False: 'no prazo'})

df_test = pedidos_entregues.merge(
    comentarios[['id_pedido', 'nota_avaliacao']],
    on='id_pedido',
    how='inner'
)

# ============================================
# 4. ANÁLISE 1 — ATRASO
# ============================================

print("\n=== ATRASO ===")

df_test['satisfeito'] = (df_test['nota_avaliacao'] >= 4).astype(int)

print(df_test.groupby('status entrega')['satisfeito'].mean())

grupo_atrasado = df_test[df_test['status entrega'] == 'atrasado']['nota_avaliacao']
grupo_prazo = df_test[df_test['status entrega'] == 'no prazo']['nota_avaliacao']

print(ttest_ind(grupo_atrasado, grupo_prazo, equal_var=False))

sns.countplot(
    data=df_test,
    x='nota_avaliacao',
    hue='status entrega',
    hue_order=['atrasado', 'no prazo']
)

plt.title('Distribuição da Nota de Avaliação por Status de Entrega')
plt.xlabel('Nota de Avaliação')
plt.ylabel('Quantidade de Pedidos')
plt.show()

# ============================================
# 5. ANÁLISE 2 — TEMPO DE ENTREGA
# ============================================

print("\n=== TEMPO DE ENTREGA ===")

df_test['timestamp_compra_pedido'] = pd.to_datetime(
    df_test['timestamp_compra_pedido'], errors='coerce'
)

df_test['tempo_entrega_dias'] = (
    df_test['data_entrega_cliente_pedido'] -
    df_test['timestamp_compra_pedido']
).dt.days

# Correlação
print("\nCorrelação tempo x nota:")
print(df_test[['tempo_entrega_dias', 'nota_avaliacao']].corr())

# Faixas
df_test['faixa_tempo'] = pd.cut(
    df_test['tempo_entrega_dias'],
    bins=[0, 3, 7, 14, 30, 100],
    labels=['0-3', '4-7', '8-14', '15-30', '30+']
)

# Garantir ordem
df_test['faixa_tempo'] = pd.Categorical(
    df_test['faixa_tempo'],
    categories=['0-3', '4-7', '8-14', '15-30', '30+'],
    ordered=True
)

# Média geral
df_tempo = df_test.groupby('faixa_tempo')['nota_avaliacao'].mean()
print(df_tempo)

plt.figure()
df_tempo.plot(marker='o')
plt.title('Nota Média por Tempo de Entrega')
plt.xlabel('Tempo de Entrega (dias)')
plt.ylabel('Nota Média')
plt.grid()
plt.show()

# Separado - no prazo
df_prazo = df_test[df_test['status entrega'] == 'no prazo'].copy()

df_prazo['faixa_tempo'] = pd.Categorical(
    df_prazo['faixa_tempo'],
    categories=['0-3', '4-7', '8-14', '15-30', '30+'],
    ordered=True
)

df_tempo_prazo = df_prazo.groupby('faixa_tempo')['nota_avaliacao'].mean()

plt.figure()
df_tempo_prazo.plot(marker='o')
plt.title('Nota Média por Tempo de Entrega (Pedidos no Prazo)')
plt.xlabel('Tempo de Entrega (dias)')
plt.ylabel('Nota Média')
plt.ylim(0, 5)
plt.grid()
plt.show()

# Separado - atrasado
df_atrasado = df_test[df_test['status entrega'] == 'atrasado'].copy()

df_atrasado['faixa_tempo'] = pd.Categorical(
    df_atrasado['faixa_tempo'],
    categories=['0-3', '4-7', '8-14', '15-30', '30+'],
    ordered=True
)

df_tempo_atrasado = df_atrasado.groupby('faixa_tempo')['nota_avaliacao'].mean()

plt.figure()
df_tempo_atrasado.plot(marker='o')
plt.title('Nota Média por Tempo de Entrega (Pedidos Atrasados)')
plt.xlabel('Tempo de Entrega (dias)')
plt.ylabel('Nota Média')
plt.ylim(0, 5)
plt.grid()
plt.show()

# ============================================
# 6. ANÁLISE 3 — FRETE
# ============================================

print("\n=== FRETE ===")

frete_por_pedido = itens.groupby('id_pedido')['valor_frete'].sum().reset_index()

df_test = df_test.merge(frete_por_pedido, on='id_pedido', how='left')

# Correlação
print("\nCorrelação frete x nota:")
print(df_test[['valor_frete', 'nota_avaliacao']].corr())

# Faixas
df_test['faixa_frete'] = pd.cut(
    df_test['valor_frete'],
    bins=[0, 10, 20, 50, 100, 1000],
    labels=['0-10', '10-20', '20-50', '50-100', '100+']
)

df_test['faixa_frete'] = pd.Categorical(
    df_test['faixa_frete'],
    categories=['0-10', '10-20', '20-50', '50-100', '100+'],
    ordered=True
)

df_frete = df_test.groupby('faixa_frete')['nota_avaliacao'].mean()
print(df_frete)

plt.figure()
df_frete.plot(marker='o')
plt.title('Nota Média por Faixa de Frete')
plt.xlabel('Faixa de Frete')
plt.ylabel('Nota Média')
plt.ylim(0, 5)
plt.grid()
plt.show()

# ============================================
# 7. CONCLUSÃO
# ============================================

print("\n=== CONCLUSÃO ===")

print("""
O cumprimento do prazo é o principal fator de satisfação do cliente.
O tempo de entrega também impacta negativamente a experiência.
O valor do frete possui impacto menor em comparação aos fatores logísticos.
""")
