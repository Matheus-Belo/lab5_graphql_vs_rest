from dotenv import load_dotenv
import requests
import csv
import os
import time
import tqdm

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
    return response.json()

def get_all_repos():
    cursor = None
    repos = []
    while True:
        response_data = get_repositories(cursor)
        
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

    return repos

def write_to_csv(repos):
    with open('./scripts/graphql/graphql.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def write_time_csv(inicio, fim):
    tempo = fim - inicio
    with open('./scripts/resultados/tempoGRAPHQL.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ferramenta', 'tempoDeExecucao'])
        writer.writerow(['GraphQl',tempo])

def main():
    inicio = time.time()
    repos = get_all_repos()
    fim = time.time()
    write_to_csv(repos)
    write_time_csv(inicio, fim)

if __name__ == "__main__":
    main()