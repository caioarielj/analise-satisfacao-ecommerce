# Análise de Satisfação do Cliente - E-commerce

## Objetivo

Este projeto tem como objetivo identificar os principais fatores que impactam a satisfação do cliente no e-commerce, com foco na experiência de entrega.

A análise busca responder à seguinte pergunta:

O que mais influencia a satisfação do cliente: atraso, tempo de entrega ou valor do frete?

## Fatores analisados

- Cumprimento do prazo de entrega  
- Tempo total de entrega  
- Valor do frete  

## Principais insights

- Atrasos na entrega reduzem significativamente a satisfação do cliente (de aproximadamente 83% para 35%)
- O tempo de entrega impacta negativamente a experiência, principalmente em prazos mais longos
- O valor do frete possui impacto menor quando comparado aos fatores logísticos

## Estrutura do projeto

analise-satisfacao-ecommerce/

├── analise_satisfacao.py  
├── README.md  
└── data/  

## Como executar

1. Crie uma pasta chamada `data` na raiz do projeto

2. Adicione os arquivos CSV dentro da pasta `data`

3. Execute o script:

python analise_satisfacao.py

## Observação sobre os dados

Os arquivos de dados não estão incluídos neste repositório.

Para executar a análise, é necessário obter os dados separadamente e inseri-los na pasta `data`.

Os dados utilizados são baseados no dataset público da Olist. Para facilitar a leitura do código, os arquivos foram renomeados da seguinte forma:

- olist_orders_dataset.csv → pedidos.csv  
- olist_order_reviews_dataset.csv → comentarios.csv  
- olist_order_items_dataset.csv → itens_do_pedido.csv  

Certifique-se de utilizar esses nomes ao executar o script.

## Tecnologias utilizadas

- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- SciPy  

## Conclusão

Os resultados indicam que a confiabilidade da entrega, especialmente o cumprimento do prazo, é o principal fator de satisfação do cliente no e-commerce.

Melhorias na performance logística tendem a gerar impacto direto na experiência do cliente, retenção e crescimento do negócio.
