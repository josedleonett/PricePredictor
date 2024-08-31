import requests
from datetime import datetime

from utils.print_console import print_console
from config import DOLAR_BLUE_API_URL, DOLAR_BLUE_API_TOKEN

# Parámetros
api_url = DOLAR_BLUE_API_URL
token = DOLAR_BLUE_API_TOKEN

headers = {
    "Authorization": "Bearer " + token
}

def get_dolar_blue():
    """
    Obtiene los datos de la API y los retorna una lista de diccionarios con fecha y valor si la solicitud fue exitosa, 
    False en caso contrario
    """
    # Hacer la solicitud a la API
    response = requests.get(api_url, headers=headers)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()

        # Procesar los datos
        processed_data = []
        for item in data:
            # Convertir la fecha al formato YYYY-MM-DD
            date = datetime.strptime(item["d"], "%Y-%m-%d").strftime("%Y-%m-%d")

            # Convertir el valor al formato con coma como separador decimal
            value = f"{item['v']:.1f}"

            # Añadir el dato procesado a la lista
            processed_data.append({"fecha": date, "valor": value})

        print_console("", "Dolar Blue obtenido correctamente")
        return processed_data
    else:
        print_console("error", "Error al obtener los datos de la API Dolar Blue: " + str(response.status_code))
        return False
