import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')


def obtener_top_10_actores(api_key, paginas=5, max_actores=10, preset=None, **parametros):
    presets = {
        "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 345,"primary_release_date.gte": "2014-01-01",
        "primary_release_date.lte": "2024-12-31"},
        "usa": {"language": "en-US", "with_origin_country": "US", "vote_count.gte": 1000},
        "arg": {"language": "es-AR", "with_origin_country": "AR", "vote_count.gte": 300}
    }

    params = {
        "sort_by": "vote_average.desc",
        **(presets[preset] if preset in presets else {}),
        **parametros
    }

    url_discover = "https://api.themoviedb.org/3/discover/movie"
    url_credits = "https://api.themoviedb.org/3/movie/{}/credits"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    actores_frecuentes = {}

    for pagina in range(1, paginas + 1):
        params["page"] = pagina
        response = requests.get(url_discover, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error en la página {pagina}: {response.status_code}")
            continue

        data = response.json()
        resultados = data.get("results", [])
        for pelicula in resultados:
            movie_id = pelicula.get("id")
            credit_response = requests.get(url_credits.format(movie_id), headers=headers)
            if credit_response.status_code != 200:
                continue

            credit_data = credit_response.json()
            cast_list = credit_data.get("cast", [])[:max_actores]
            for actor in cast_list:
                nombre = actor.get("name", "Desconocido")
                actores_frecuentes[nombre] = actores_frecuentes.get(nombre, 0) + 1

    # Función
    actores_ordenados = sorted(actores_frecuentes.items(), key=lambda x: x[1], reverse=True)[:10]

    # diccionario
    top_10_actores = dict(actores_ordenados)

    return top_10_actores


