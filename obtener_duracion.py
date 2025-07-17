import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

def obtener_duracion_top_peliculas(api_key, paginas=5, preset=None, **presets):
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
                    print(f"{contador}. {titulo} ({anio}) - Duración: {duracion} min")
                else:
                    print(f"{contador}. {titulo} ({anio}) - Duración: no se pudo obtener 😕")
                contador += 1
        else:
            print(f"Error en la página {pagina}: {response.status_code}")
            break

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

obtener_duracion_top_peliculas(api_key, paginas=5, preset="esp")