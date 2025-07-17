import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

def obtener_peliculas_filtradas(api_key, query, min_votos=0, pais=None, nombre_compania=None, paginas=1):
    datos_peliculas = []
    
    url_search = "https://api.themoviedb.org/3/search/movie"
    url_detalles = "https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    contador = 1

    for pagina in range(1, paginas + 1):
        params = {
            "query": query,
            "page": pagina,
            "language": "es-ES"
        }

        response = requests.get(url_search, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error en búsqueda: {response.status_code}")
            break

        resultados = response.json().get("results", [])

        for pelicula in resultados:
            if not pelicula.get("id"):
                continue

            movie_id = pelicula["id"]

            # Obtener detalles completos
            detalle = requests.get(url_detalles.format(movie_id=movie_id), headers=headers).json()

            # Filtros
            if detalle.get("vote_count", 0) < min_votos:
                continue

            if pais not in detalle.get("origin_country", []):
                continue

            companias = [c["name"].lower() for c in detalle.get("production_companies", [])]
            if nombre_compania and nombre_compania.lower() not in " ".join(companias):
                continue

            titulo = detalle.get("title", "Sin título")
            puntuacion = detalle.get("vote_average", "N/A")
            anio = detalle.get("release_date", "Desconocido")[:4]
            print(f"{contador}. {titulo} ({anio}) - Puntuación: {puntuacion}")
            contador += 1

            datos_peliculas.append({"titulo": titulo,
                                    "anio": anio,
                                    "puntuacion": puntuacion,
                                    "votos": detalle.get("vote_count",0),
                                    "pais": detalle.get("origin_country", []),
                                    "productora": ", ".join(companias)
                                    })
                                    
    return datos_peliculas

# Tu API key
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

# Ejemplo: buscar "Fate", mínimo 100 votos, del país JP, y producidas por Aniplex
peliculas = obtener_peliculas_filtradas(
    api_key,
    query="Fate",
    min_votos=100,
    pais="JP",
    nombre_compania="Aniplex",
    paginas=1
)


print(peliculas)

