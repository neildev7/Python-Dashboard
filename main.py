import streamlit as st      # Importa o Streamlit para criar o dashboard web
import pandas as pd         # Importa o pandas para manipulação de dados

# Lê o arquivo Excel chamado 'vendas.xlsx' e armazena os dados em uma tabela (DataFrame)
tabela = pd.read_excel('vendas.xlsx')

# Mostra a tabela no terminal (apenas para debug, não aparece no dashboard)
print(tabela)

# Título do dashboard na página web
st.title('Dashboard de Vendas')

# Cria um filtro para o usuário escolher as regiões que quer ver
regioes = st.multiselect('Selecione as regiões', tabela['Região'].unique())

# Se o usuário selecionar alguma região, filtra a tabela para mostrar só essas regiões
if regioes:
    tabela = tabela[tabela["Região"].isin(regioes)]

# Calcula o faturamento total (soma de todas as vendas)
total_faturamento = tabela["Valor Venda"].sum()
# Mostra o faturamento total no dashboard
st.metric('Faturamento Total', f'R$ {total_faturamento:,.2f}')

# Calcula o ticket médio (média dos valores de venda)
ticket_medio = tabela["Valor Venda"].mean()
# Se não houver vendas, mostra 0 em vez de NaN
if pd.isna(ticket_medio):
    ticket_medio = 0.0
# Mostra o ticket médio no dashboard
st.metric('Ticket Médio', f'R$ {ticket_medio:,.2f}')

# Gráfico de faturamento por região (soma das vendas por cada região)
grafico_regiao = tabela.groupby("Região")["Valor Venda"].sum().reset_index()
st.bar_chart(grafico_regiao.set_index("Região"))

# Gráfico de faturamento por produto (soma das vendas por cada produto)
grafico_produto = tabela.groupby("Produto")["Valor Venda"].sum().reset_index()
st.bar_chart(grafico_produto.set_index("Produto"))

# Gráfico de faturamento por mês (série temporal)
# Converte a coluna 'Data' para o formato de data
tabela['Data'] = pd.to_datetime(tabela['Data'], errors='coerce')
# Agrupa as vendas por mês e soma os valores
grafico_mes = tabela.groupby(tabela['Data'].dt.to_period("M"))["Valor Venda"].sum().reset_index()
# Ajusta o formato da data para aparecer corretamente no gráfico
grafico_mes['Data'] = grafico_mes['Data'].dt.to_timestamp()
# Mostra o gráfico de linha com o faturamento por mês
st.line_chart(grafico_mes.set_index("Data"))