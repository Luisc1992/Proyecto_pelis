import requests

API_KEY = '262d626fe3b226093c5317116a15c786'
BASE_URL = 'https://api.themoviedb.org/3'

def buscar_por_id(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'es-ES'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        pelicula = response.json()
        print(f"Título: {pelicula['title']}")
        print(f"Fecha de estreno: {pelicula['release_date']}")
        print(f"Descripción: {pelicula['overview']}")
        print(f"Puntuación promedio: {pelicula['vote_average']}")
    else:
        print(f"Error {response.status_code} - {response.json().get('status_message')}")

# Buscar por ID
buscar_por_id(238)  # 238 = El Padrino
