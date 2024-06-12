import requests
import csv
import os
import time
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a chave de acesso do GitHub
chave = os.getenv("key")
url = 'https://api.github.com/search/repositories'
headers = {'Authorization': f'token {chave}'}

def get_repositories(language=None, since="2023-01-01T00:00:00Z", page=1, per_page=100, timeout=10):
    params = {
        'q': f'stars:>0',
        'sort': 'stars',
        'order': 'desc',
        'per_page': per_page,
        'page': page
    }
    if language:
        params['q'] += f' language:{language}'
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    return response

def get_all_repos():
    repos = []
    total_bytes = 0
    for language in ['python', '']:
        page = 1
        response = get_repositories(language=language, page=page)
        response.raise_for_status()
        total_bytes += measure_response_size(response)
        
        response_data = response.json()
        
        if 'errors' in response_data:
            print("Erro na solicitação:", response_data['errors'])
        elif 'items' in response_data:
            for item in response_data['items']:
                repository_info = {
                    'nameWithOwner': item['full_name'],
                    'createdAt': item['created_at'],
                    'stargazerCount': item['stargazers_count'],
                }
                repos.append(repository_info)
    return repos, total_bytes

def measure_response_size(response):
    try:
        size_bytes = len(response.content)
        return size_bytes
    except Exception as e:
        print("Erro ao medir o tamanho da resposta:", e)
        return None

def write_to_csv(repos):
    with open('./scripts/rest/rest.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def write_time_csv(inicio, fim, total_bytes):
    tempo = fim - inicio
    with open('./scripts/resultados/REST.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)   
        if csvfile.tell() == 0:
            writer.writerow(['Ferramenta', 'tempoDeExecucao', 'totalBytes'])
        writer.writerow(['REST', tempo, total_bytes])

def main():
    i = 0
    while i < 5:
        inicio = time.time()
        repos, total_bytes = get_all_repos()
        fim = time.time()
        write_to_csv(repos)
        write_time_csv(inicio, fim, total_bytes)
        i += 1


if __name__ == "__main__":
    main()