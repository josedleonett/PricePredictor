# Crear un archivo de configuración para almacenar las variables de entorno

import os
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno 

BASE_API_URL = os.getenv("PP_BASE_API_URL")
BASE_API_TOKEN = os.getenv("PP_BASE_API_TOKEN")

print(BASE_API_URL, BASE_API_TOKEN)

# Variables de entorno para la API de DolarBlue
DOLAR_BLUE_API_URL = os.getenv("DOLAR_BLUE_API_URL")
DOLAR_BLUE_API_TOKEN = os.getenv("DOLAR_BLUE_API_TOKEN")

# Variables de entorno para la API de DolarOficial
DOLAR_OFICIAL_API_URL = os.getenv("DOLAR_OFICIAL_API_URL")
DOLAR_OFICIAL_API_TOKEN = os.getenv("DOLAR_OFICIAL_API_TOKEN")

# Variables de entorno para la API de la InflacionMensualOficial
INFLACION_OFICIAL_API_URL = os.getenv("INFLACION_OFICIAL_API_URL")
INFLACION_OFICIAL_API_TOKEN = os.getenv("INFLACION_OFICIAL_API_TOKEN")

