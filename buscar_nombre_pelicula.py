import requests

# La clave API de TMDB
API_KEY = '262d626fe3b226093c5317116a15c786'
# URL base de la API
BASE_URL = 'https://api.themoviedb.org/3'

# Ejemplo: buscar una película
def buscar_pelicula(nombre_pelicula):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': nombre_pelicula,
        'language': 'es-ES'  # Opcional: para obtener resultados en español
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        datos = response.json()
        for i, pelicula in enumerate(datos['results'][:5], 1):
            print(f"{i}. {pelicula['title']} ({pelicula['release_date']})")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Ejecutar la búsqueda
buscar_pelicula("Spiderman")
