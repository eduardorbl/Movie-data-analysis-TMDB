import requests
import sys
import os
from dotenv import load_dotenv

def get_genres():
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")  # Obtém a chave da API das variáveis de ambiente

    # URL da API para obter os gêneros
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Fazendo a requisição
    response = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro ao buscar dados da API: {response.status_code}")
        sys.exit(1)
    else:
        # Extrai os dados da resposta
        genres_data = response.json()
        genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}
        return genres_dict
