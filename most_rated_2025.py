import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")   # << línea mágica

API_KEY = '262d626fe3b226093c5317116a15c786'
BASE_URL = 'https://api.themoviedb.org/3'

def obtener_contenido_2025(tipo):
    if tipo not in ("movie", "tv"):
        print("Tipo inválido. Usa 'movie' o 'tv'.")
        return

    url = f"{BASE_URL}/discover/{tipo}"
    params = {
        "api_key": API_KEY,
        "language": "es-ES",
        "sort_by": "popularity.desc",
        "vote_count.gte": 10,
        "page": 1,
        ("primary_release_year" if tipo == "movie" else "first_air_date_year"): 2025
    }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f"Error {r.status_code}: {r.json().get('status_message')}")
        return

    for i, item in enumerate(r.json()["results"][:10], 1):
        titulo = item.get("title") or item.get("name")
        fecha  = item.get("release_date") or item.get("first_air_date")
        print(f"{i}. {titulo} ({fecha}) - Puntuación: {item['vote_average']}")

print("Películas 2025:")
obtener_contenido_2025("movie")
print("\nSeries 2025:")
obtener_contenido_2025("tv")
