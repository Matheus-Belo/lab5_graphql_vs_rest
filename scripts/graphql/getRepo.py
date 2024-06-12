from dotenv import load_dotenv
import requests
import csv
import os
import time

load_dotenv()

chave = os.getenv('key')
url = 'https://api.github.com/graphql'
headers = {'Authorization': 'Bearer %s' % chave}

query = """
query($cursor: String) {
  search(query: "stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        stargazerCount
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

query2 = """
query($cursor: String) {
  search(query: " language python stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        stargazerCount
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

def get_repositories(cursor=None):
    response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
    response_bytes = response.content
    return response.json(), len(response_bytes)

def get_all_repos():
    cursor = None
    repos = []
    total_bytes = 0
    while True:
        response_data, response_size = get_repositories(cursor)
        total_bytes += response_size

        # Verifica se a solicitação foi bem-sucedida
        if 'errors' in response_data:
            print("Erro na solicitação:", response_data['errors'])
            break

        # Verifica se a chave 'data' está presente na resposta
        if 'data' in response_data:
            for node in response_data['data']['search']['nodes']:
                repository_info = {
                    'nameWithOwner': node['nameWithOwner'],
                    'createdAt' : node['createdAt'],
                    'stargazerCount': node['stargazerCount'],
                }
                repos.append(repository_info)
            pageInfo = response_data['data']['search']['pageInfo']
            hasNextPage = pageInfo['hasNextPage']
            if not hasNextPage or len(repos) >= 100:
                break
            cursor = pageInfo['endCursor']
        else:
            print("Resposta inesperada:", response_data)
            break

    return repos, total_bytes

def write_repo_csv(repos):
    with open('./scripts/graphql/graphql.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def write_result_csv(inicio, fim, total_bytes):
    tempo = fim - inicio

    file_path = './scripts/resultados/GRAPHQL.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:

        writer = csv.writer(csvfile)
        
        # Se o arquivo não existia, escreva o cabeçalho
        if not file_exists:
            writer.writerow(['Ferramenta', 'tempoDeExecucao', 'totalBytes'])
        
        writer.writerow(['GraphQl', tempo, total_bytes])

def main():
    i = 0
    while i < 25:
        inicio = time.time()
        repos, total_bytes = get_all_repos()
        fim = time.time()
        write_repo_csv(repos)
        write_result_csv(inicio, fim, total_bytes)
        i+=1;

if __name__ == "__main__":
    main()
