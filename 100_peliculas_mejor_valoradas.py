import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

def obtener_top_peliculas(api_key,paginas=5,preset=None,**presets):

    url = "https://api.themoviedb.org/3/discover/movie"

    presets_dict = {
    "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 345,"primary_release_date.gte": "2014-01-01",
"primary_release_date.lte": "2024-12-31"},
    "usa": {"language": "en-US", "with_origin_country": "US", "vote_count.gte": 1000},
    "arg": {"language": "es-AR", "with_origin_country": "AR", "vote_count.gte": 300}
    }

    params = {
                "sort_by": "vote_average.desc",
                **(presets_dict[preset] if preset in presets_dict else {}),
                **presets
            }

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"
    }

    contador = 1

    for pagina in range(1, paginas + 1):  # Páginas de la 1 a la 5 = hasta 100 resultados (20 por página)
        params["page"] = pagina
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])

            for pelicula in resultados:
                titulo = pelicula.get("title", "Sin título")
                puntuacion = pelicula.get("vote_average", "N/A")
                anio = pelicula.get("release_date", "Desconocido")[:4]
                print(f"{contador}. {titulo} ({anio}) - Puntuación: {puntuacion}")
                contador += 1
        else:
                print(f"Error en la página {pagina}: {response.status_code}")
                break


api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

obtener_top_peliculas(api_key, paginas=5,preset="esp")