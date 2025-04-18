import os
import tweepy
import pandas as pd
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cargar variables de entorno (para pruebas locales)
load_dotenv()

# Acceder a las variables de entorno
try:
    api_key = os.environ["API_KEY"]  # Clave de la API
    api_secret = os.environ["API_SECRET"]  # Secreto de la API
    access_token = os.environ["ACCESS_TOKEN"]  # Token de acceso
    access_secret = os.environ["ACCESS_SECRET"]  # Secreto del token de acceso
except KeyError as e:
    logging.error(f"Error: La variable de entorno {e} no está configurada.")
    raise


def publicar_tweet(df_transformado):
    """
    Publica un tweet con la información del DataFrame
    Args:
        df_transformado: DataFrame con los datos procesados
    Returns:
        bool: True si el tweet se publicó correctamente, False en caso contrario
    """
    if df_transformado is None:
        logging.error("No hay datos disponibles para publicar")
        return False

    # Autenticación en API v2
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

    # Preparar los datos para el tweet
    df_transformado["Date"] = pd.to_datetime(df_transformado["Date"])
    ultimo_mes = df_transformado["Date"].max()
    mes_anterior = ultimo_mes - pd.DateOffset(months=1)

    # Filtrar datos solo del último mes y del mes anterior
    df_filtered = df_transformado[
        df_transformado["Date"].dt.to_period("M").isin([mes_anterior.to_period("M"), ultimo_mes.to_period("M")])
    ]

    # Calcular promedio de precios por región y fecha
    df_promedios = df_filtered.groupby(["Región", "Date"])["Price"].mean().reset_index()

    # Ordenar y calcular la variación porcentual del último mes para cada región
    df_promedios = df_promedios.sort_values(by=["Región", "Date"])
    df_promedios["Variación"] = df_promedios.groupby("Región")["Price"].pct_change() * 100

    # Filtrar solo los valores del último mes para las regiones
    df_final = df_promedios[df_promedios["Date"] == ultimo_mes]

    # Calcular la variación IPC promedio de todos los productos seleccionados (por región)
    inflacion_promedio = df_final["Variación"].mean()

    # Ordenar df_final por la variación en orden descendente
    df_final = df_final.sort_values(by="Variación", ascending=False)

    # Obtener el producto seleccionado con mayor alza y mayor baja a nivel general (último mes)
    # Se utilizan los datos filtrados para el último mes a nivel de "Productos seleccionados"
    df_productos = df_filtered.groupby(["Productos seleccionados", "Date"])["Price"].mean().reset_index()
    df_productos = df_productos.sort_values(by=["Productos seleccionados", "Date"])
    df_productos["Variación"] = df_productos.groupby("Productos seleccionados")["Price"].pct_change() * 100
    df_productos_final = df_productos[df_productos["Date"] == ultimo_mes]
    mayor_alza_producto = df_productos_final.loc[df_productos_final["Variación"].idxmax()]
    mayor_baja_producto = df_productos_final.loc[df_productos_final["Variación"].idxmin()]

    # Obtener el último mes en formato de texto
    ultimo_mes_str = ultimo_mes.strftime("%B %Y") \
        .replace("January", "Enero").replace("February", "Febrero") \
        .replace("March", "Marzo").replace("April", "Abril") \
        .replace("May", "Mayo").replace("June", "Junio") \
        .replace("July", "Julio").replace("August", "Agosto") \
        .replace("September", "Septiembre").replace("October", "Octubre") \
        .replace("November", "Noviembre").replace("December", "Diciembre")

    tweet_text = f"INDEC CANASTA IPC {ultimo_mes_str}: {inflacion_promedio:.2f}% \n"
    tweet_text += "\n📊Región:\n"
    for _, row in df_final.iterrows():
        emoji = "📉" if row["Variación"] < 0 else "📈"
        tweet_text += f"🔹 {row['Región']}: {row['Variación']:.2f}% \n"

    # Agregar información sobre la variación de productos (último mes)
    tweet_text += f"\n📈Cambios:\n"
    tweet_text += f"🔼: {mayor_alza_producto['Productos seleccionados']} +{mayor_alza_producto['Variación']:.2f}%\n"
    tweet_text += f"🔽: {mayor_baja_producto['Productos seleccionados']} {mayor_baja_producto['Variación']:.2f}%\n"
    tweet_text += "\n🤖Github/Mauricioarcez"

    # Publicar el tweet
    try:
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Tweet publicado: https://twitter.com/user/status/{response.data['id']}")
        return True
    except Exception as e:
        print(f"❌ Error al publicar el tweet: {e}")
        return False

