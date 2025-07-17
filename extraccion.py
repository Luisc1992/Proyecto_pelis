from top_actores import obtener_top_10_actores
from peliculas_top_100 import obtener_top_peliculas
from revenue_peliculas import obtener_beneficios


api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"

top_10_dict = obtener_top_10_actores(api_key, preset="esp", paginas=5, max_actores=10)



peliculas = obtener_top_peliculas(api_key, paginas=5, preset="esp")


