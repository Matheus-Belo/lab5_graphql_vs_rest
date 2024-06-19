import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminhos relativos para os novos arquivos CSV
data_rest_path = 'scripts\\resultados\\RESTquery2.csv'
data_graphql_path = 'scripts\\resultados\\GRAPHQLquery2.csv'

# Verifique se os arquivos CSV existem
if not os.path.exists(data_rest_path):
    raise FileNotFoundError(f"O arquivo {data_rest_path} não foi encontrado.")
if not os.path.exists(data_graphql_path):
    raise FileNotFoundError(f"O arquivo {data_graphql_path} não foi encontrado.")

# Ler os arquivos CSV
data_rest = pd.read_csv(data_rest_path)
data_graphql = pd.read_csv(data_graphql_path)

# Adicionar uma coluna para identificar a ferramenta
data_rest['Ferramenta'] = 'REST'
data_graphql['Ferramenta'] = 'GraphQl'

# Adicionar uma coluna de índice para unir os dados corretamente
data_rest['Index'] = data_rest.index
data_graphql['Index'] = data_graphql.index

# Combinar os dados em um único DataFrame
data = pd.concat([data_rest, data_graphql])

# Definir a pasta para salvar os gráficos
output_folder = os.path.join('..', 'scripts', 'resultados', 'graficos')
os.makedirs(output_folder, exist_ok=True)

# Definir o estilo dos gráficos
sns.set(style="whitegrid")

# Paleta de cores personalizada
palette = {
    'REST': 'red',
    'GraphQl': 'blue'
}

# Criar um gráfico de barras para o tempo de execução
plt.figure(figsize=(12, 6))
sns.barplot(x='Index', y='tempoDeExecucao', hue='Ferramenta', data=data, palette=palette)
plt.title('Tempo de Execução')
plt.ylabel('Tempo de Execução (segundos)')
plt.xlabel('Execução')
plt.legend(title='Ferramenta')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'tempo_execucao_comparacao.png'))
plt.show()

# Calcular o total de bytes médio por ferramenta
mean_total_bytes = data.groupby('Ferramenta')['totalBytes'].mean().reset_index()

# Criar um gráfico de barras para o total de bytes médio
plt.figure(figsize=(10, 6))
sns.barplot(x='Ferramenta', y='totalBytes', data=mean_total_bytes, palette=palette)
plt.title('Total de Bytes Médio entre REST e GraphQL')
plt.ylabel('Total de Bytes')
plt.xlabel('Ferramenta')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'total_bytes_medio.png'))
plt.show()