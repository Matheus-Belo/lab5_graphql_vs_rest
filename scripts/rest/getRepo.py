from dotenv import load_dotenv
import requests
import csv
import os
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a chave de acesso do GitHub
chave = os.getenv("key")
url = 'https://api.github.com/search/repositories'
headers = {'Authorization': f'token {chave}'}

def get_repositories(since="2023-01-01T00:00:00Z", page=1, per_page=100):
    params = {
        'q': 'stars:>0',
        'sort': 'stars',
        'order': 'desc',
        'per_page': per_page,
        'page': page
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_all_repos():
    repos = []
    page = 1
    while True:
        response_data = get_repositories(page=page)
        
        # Verifica se a solicitação foi bem-sucedida
        if 'errors' in response_data:
            print("Erro na solicitação:", response_data['errors'])
            break
        
        # Verifica se a chave 'items' está presente na resposta
        if 'items' in response_data:
            for item in response_data['items']:
                repository_info = {
                    'nameWithOwner': item['full_name'],
                    'createdAt': item['created_at'],
                    'stargazerCount': item['stargazers_count'],
                }
                repos.append(repository_info)
            if len(response_data['items']) >= 100:
                break
            page += 1
        else:
            print("Resposta inesperada:", response_data)
            break

    return repos

def write_to_csv(repos):
    with open('./scripts/rest/rest.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def write_time_csv(inicio, fim):
    tempo = fim - inicio
    with open('./scripts/resultados/tempoREST.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ferramenta', 'tempoDeExecucao'])
        writer.writerow(['REST', tempo])

def main():
    inicio = time.time()
    repos = get_all_repos()
    fim = time.time()
    write_to_csv(repos)
    write_time_csv(inicio, fim)

if __name__ == "__main__":
    main()