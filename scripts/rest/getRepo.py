from dotenv import load_dotenv
import requests
import csv
import os
import time

load_dotenv()

chave = os.getenv('key')
url = 'https://api.github.com/search/repositories'
headers = {'Authorization': 'Bearer %s' % chave}

def get_repositories_rest(page):
    params = {
        'q': 'stars:>0',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 100,
        'page': page
    }
    response = requests.get(url, headers=headers, params=params)
    response_bytes = response.content
    return response.json(), len(response_bytes)

def get_all_repos_rest():
    page = 1
    repos = []
    total_bytes = 0
    while True:
        response_data, response_size = get_repositories_rest(page)
        total_bytes += response_size

        # Verifica se a solicitação foi bem-sucedida
        if 'errors' in response_data:
            print("Erro na solicitação:", response_data['errors'])
            break

        # Verifica se a chave 'items' está presente na resposta
        if 'items' in response_data:
            for item in response_data['items']:
                repository_info = {
                    'nameWithOwner': item['full_name'],
                    'createdAt' : item['created_at'],
                    'stargazerCount': item['stargazers_count'],
                }
                repos.append(repository_info)
            if len(response_data['items']) < 100 or len(repos) >= 100:
                break
            page += 1
        else:
            print("Resposta inesperada:", response_data)
            break

    return repos, total_bytes

def write_repo_csv(repos):
    with open('./scripts/rest/rest.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def write_result_csv(inicio, fim, total_bytes):
    tempo = fim - inicio

    file_path = './scripts/resultados/RESTquery.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Se o arquivo não existia, escreva o cabeçalho
        if not file_exists:
            writer.writerow(['Ferramenta', 'tempoDeExecucao', 'totalBytes'])
        
        writer.writerow(['REST', tempo, total_bytes])

def main():
    i = 0
    while i < 5:
        inicio = time.time()
        repos, total_bytes = get_all_repos_rest()
        fim = time.time()
        write_repo_csv(repos)
        write_result_csv(inicio, fim, total_bytes)
        i += 1

if __name__ == "__main__":
    main()