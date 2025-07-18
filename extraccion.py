from funciones import obtener_top_peliculas,obtener_top_10_actores,obtener_duracion_top_peliculas,contar_generos_top_peliculas,obtener_beneficios
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjJkNjI2ZmUzYjIyNjA5M2M1MzE3MTE2YTE1Yzc4NiIsIm5iZiI6MTc1MjA2OTAzNi44NTIsInN1YiI6IjY4NmU3M2FjYTcyMmQzODk0YjEwNDYzZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbNiPXVBiDP8jr7KPcJg0YXkttw5T7nJqnkgNVPwKr8"


top_10 = obtener_top_10_actores(api_key, preset="esp", paginas=5, max_actores=10)
#print(top_10)

peliculas = obtener_top_peliculas(api_key, paginas=5, preset="esp")
#print(peliculas)
generos = contar_generos_top_peliculas(api_key, paginas=5, preset="esp")
#print(generos)
duracion = obtener_duracion_top_peliculas(api_key, paginas=5, preset="esp")
#print(duracion)
beneficios = obtener_beneficios()
#print(beneficios)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suponiendo que ya has obtenido las películas
peliculas = obtener_top_peliculas(api_key, paginas=5, preset="esp")

# Paso 1: Convertir a DataFrame y limpiar datos
df = pd.DataFrame(peliculas)

df['puntuacion'] = pd.to_numeric(df['puntuacion'], errors='coerce')
df['anio'] = pd.to_numeric(df['anio'], errors='coerce')

df.dropna(subset=['anio', 'puntuacion'], inplace=True)


# Paso 2: Agrupar por año y calcular media
df_media_anual = df.groupby('anio')['puntuacion'].mean().reset_index()


import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

fig = px.line(df_media_anual, 
              x='anio', 
              y='puntuacion', 
              markers=True, 
              title="Puntuación media por año")

fig.update_traces(mode='lines+markers', hovertemplate='Año: %{x}<br>Puntuación: %{y:.2f}')

# Mostrar todos los años en el eje X
fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Puntuación media",
    xaxis=dict(
        tickmode='linear',
        dtick=1  # Mostrar cada año
    )
)

fig.show()
