import requests
import csv
from datetime import datetime

# Parámetros
output_file_path = "raw_data/time_series/precio_articulo.csv"


def get_precio_articulo():
    # Hacer la solicitud a la API
    response = requests.get(api_url, headers=headers)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()

        # Abrir un archivo CSV para escribir los datos
        with open(output_file_path, mode="w", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["fecha", "valor"])  # Escribir el encabezado

            for item in data:
                # Convertir la fecha al formato 'd/m/Y'
                date = datetime.strptime(item["d"], "%Y-%m-%d").strftime("%Y-%m-%d")

                # Convertir el valor al formato con coma como separador decimal
                value = f"{item['v']:.1f}"

                # Escribir la fila en el CSV
                writer.writerow([date, value])

        print(f"Datos exportados correctamente a '{output_file_path}'.")
        return output_file_path

    else:
        print("Error al obtener los datos de la API:", response.status_code)
        return False