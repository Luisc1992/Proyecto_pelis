import requests

API_KEY = '262d626fe3b226093c5317116a15c786'
BASE_URL = 'https://api.themoviedb.org/3'

def peliculas_mas_votadas():
    url = f"{BASE_URL}/discover/movie"
    params = {
        'api_key': API_KEY,
        'language': 'es-ES',
        'sort_by': 'vote_count.desc',
        'page': 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        datos = response.json()
        for i, pelicula in enumerate(datos['results'][:10], 1):
            titulo = pelicula['title']
            fecha = pelicula['release_date']
            puntuacion = pelicula['vote_average']
            votos = pelicula['vote_count']
            print(f"{i}. {titulo} ({fecha}) - Puntuación: {puntuacion} - Votos: {votos}")
    else:
        print(f"Error: {response.status_code} - {response.json().get('status_message')}")

# Ejecutar
peliculas_mas_votadas()
