import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

discover_url = "https://api.themoviedb.org/3/discover/movie"
details_url = "https://api.themoviedb.org/3/movie/{}"

params = {
    "language": "es-ES",
    "vote_count.gte": 500,
    "with_origin_country": "ES",
    "sort_by": "vote_average.desc"
}

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"
}

def obtener_duracion(movie_id):
    response = requests.get(details_url.format(movie_id), headers=headers)
    if response.status_code == 200:
        detalles = response.json()
        return detalles.get("runtime", "Desconocida")
    else:
        return "Desconocida"

contador = 1

for pagina in range(1, 6):  # Páginas 1 a 5
    params["page"] = pagina
    response = requests.get(discover_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        resultados = data.get("results", [])

        for pelicula in resultados:
            movie_id = pelicula.get("id")
            titulo = pelicula.get("title", "Sin título")
            puntuacion = pelicula.get("vote_average", "N/A")
            anio = pelicula.get("release_date", "Desconocido")[:4]
            duracion = obtener_duracion(movie_id)

            print(f"{contador}. {titulo} ({anio}) - Puntuación: {puntuacion} - Duración: {duracion} min")
            contador += 1
    else:
        print(f"Error en la página {pagina}: {response.status_code}")
        break