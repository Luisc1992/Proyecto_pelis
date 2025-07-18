import requests
import sys

#Funcion top 100 peliculas
sys.stdout.reconfigure(encoding='utf-8')
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

def obtener_top_peliculas(api_key, paginas=1, preset=None, **presets):
    datos_peliculas = []
    url = "https://api.themoviedb.org/3/discover/movie"

    presets_dict = {
        "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 345, "primary_release_date.gte": "2014-01-01",
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
        "Authorization": f"Bearer {api_key}"
    }

    for pagina in range(1, paginas + 1):
        params["page"] = pagina
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])

            for pelicula in resultados:
                if len(datos_peliculas) >= 10:
                    break

                titulo = pelicula.get("title", "Sin título")
                puntuacion = pelicula.get("vote_average", "N/A")
                fecha = pelicula.get("release_date", "Desconocido")
                anio = fecha[:4] if fecha != "Desconocido" and fecha else "Desconocido"

                datos_peliculas.append({
                    "titulo": titulo,
                    "puntuacion": puntuacion,
                    "anio": anio,
                })

            if len(datos_peliculas) >= 10:
                break 

        else:
            print(f"Error en la página {pagina}: {response.status_code}")
            break

    return datos_peliculas


#Funcion top_10 actores más repetidos
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

    
    actores_ordenados = sorted(actores_frecuentes.items(), key=lambda x: x[1], reverse=True)[:10]

    
    top_10_actores = dict(actores_ordenados)

    return top_10_actores

#Funcion generos_peliculas
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

    generos_peliculas.append({"nombre":nombre,"recuento": contador_generos})
    return generos_peliculas

#Funcion obtener_beneficios
def obtener_beneficios():
    beneficios = []
    url = "https://api.themoviedb.org/3/discover/movie"
    url_detail_base = "https://api.themoviedb.org/3/movie/"

    params = {
        "language": "es-ES",
        "vote_count.gte": 345,
        "with_origin_country": "ES",
        "sort_by": "vote_average.desc"
    }

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"
    }
    
    
    
    for pagina in range(1, 6):  # Páginas de la 1 a la 5 = hasta 100 resultados (20 por página)
        params["page"] = pagina
        response = requests.get(url, headers=headers, params=params)
    
        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])
    
            for pelicula in resultados:
                titulo = pelicula.get("title", "Sin título")
                puntuacion = pelicula.get("vote_average", "N/A")
                anio = pelicula.get("release_date", "Desconocido")[:4]
                pelicula_id = pelicula.get("id")
                
                
                url_detalle = f"{url_detail_base}{pelicula_id}"
                detalle_response = requests.get(url_detalle, headers=headers)
    
                if detalle_response.status_code == 200:
                    detalle_data = detalle_response.json()
                    beneficio = detalle_data.get("revenue", 0)
                    beneficio_str = f"${beneficio}" if beneficio else "Sin información"
                    beneficios.append({"titulo": titulo,
                                       "puntuacion": puntuacion,
                                       "anio":anio,
                                       "pelicula_id":pelicula_id,
                                       "beneficios":beneficio_str})
                else:
                    revenue_str = "Error al obtener"
            return beneficios
                
       
        else:
            print(f"Error en la página {pagina}: {response.status_code}")
            break

#Funcion obtener_duracion
def obtener_duracion_top_peliculas(api_key, paginas=5, preset=None, **presets):
    duracion_peliculas = []
    url = "https://api.themoviedb.org/3/discover/movie"
    url_detalle = "https://api.themoviedb.org/3/movie/"

    presets_dict = {
        "esp": {"language": "es-ES", "with_origin_country": "ES", "vote_count.gte": 345, "primary_release_date.gte": "2014-01-01", "primary_release_date.lte": "2024-12-31"},
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
        "Authorization": f"Bearer {api_key}"
    }

    contador = 1

    for pagina in range(1, paginas + 1):
        params["page"] = pagina
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])

            for peli in resultados:
                titulo = peli.get("title", "Sin título")
                peli_id = peli.get("id")
                anio = peli.get("release_date", "Desconocido")[:4]

                detalle_url = f"{url_detalle}{peli_id}"
                respuesta_detalle = requests.get(detalle_url, headers=headers, params={"language": params.get("language", "es-ES")})

                if respuesta_detalle.status_code == 200:
                    detalle = respuesta_detalle.json()
                    duracion = detalle.get("runtime", "N/A")
                    duracion_peliculas.append({"titulo":titulo,
                                               "peli_id":peli_id,
                                                "anio":anio,
                                                "duracion":duracion})
                else:
                    print(f"- Duración: no se pudo obtener")
                contador += 1
        else:
            print(f"Error en la página {pagina}: {response.status_code}")
            break
    return duracion_peliculas







