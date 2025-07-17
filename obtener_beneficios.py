import requests
import sys

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


beneficios = obtener_beneficios()

print(beneficios)