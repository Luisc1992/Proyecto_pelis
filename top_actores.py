import requests

def obtener_actores_frecuentes(api_key, paginas=5, max_actores=10, preset=None, **parametros):
    

    # Presets predefinidos
    presets = {
        "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 500},
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

    params = {
        "sort_by": "vote_average.desc",
        **parametros
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

    # Ordenar y devolver los actores más frecuentes
    actores_por_orden = sorted(actores_frecuentes.items(), key=lambda x: x[1], reverse=True)
    return actores_por_orden

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

actores_esp = obtener_actores_frecuentes(api_key, preset="esp", paginas=5, max_actores=10)
print("Top actores España:")
for nombre, cantidad in actores_esp[:5]:
    print(f"{nombre}: {cantidad} apariciones")
