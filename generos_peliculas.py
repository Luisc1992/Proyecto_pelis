import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

def contar_generos_top_peliculas(api_key, paginas=5, preset="esp", **presets):
    generos_peliculas = []
    # Paso 1: Obtener los géneros disponibles (id → nombre)
    url_generos = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response_genres = requests.get(url_generos, headers=headers, params={"language": "es-ES"})
    generos_dict = {g["id"]: g["name"] for g in response_genres.json().get("genres", [])}

    # Paso 2: Obtener películas usando el mismo preset
    url = "https://api.themoviedb.org/3/discover/movie"

    presets_dict = {
        "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 345,
                "primary_release_date.gte": "2014-01-01", "primary_release_date.lte": "2024-12-31"},
        "usa": {"language": "en-US", "with_origin_country": "US", "vote_count.gte": 1000},
        "arg": {"language": "es-AR", "with_origin_country": "AR", "vote_count.gte": 300}
    }

    params = {
        "sort_by": "vote_average.desc",
        **(presets_dict[preset] if preset in presets_dict else {}),
        **presets
    }

    contador_generos = {}

    for pagina in range(1, paginas + 1):
        params["page"] = pagina
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])
            for pelicula in resultados:
                ids = pelicula.get("genre_ids", [])
                for gid in ids:
                    nombre = generos_dict.get(gid, "Desconocido")
                    contador_generos[nombre] = contador_generos.get(nombre, 0) + 1
        else:
            print(f"Error en la página {pagina}: {response.status_code}")
            break

    generos_peliculas.append({"recuento": contador_generos})
    return generos_peliculas

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

