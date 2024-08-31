import csv
from request.get_dolar_blue import get_dolar_blue
from request.get_dolar_oficial import get_dolar_oficial
from request.get_inflacion_mensual_oficial import get_inflacion_mensual_oficial
from utils.print_console import print_console


def update_data():
    """
    Obtiene los datos de las APIs y los guarda en la carpeta /temp
    """

    data = {
        "dolar_blue": get_dolar_blue(),
        "dolar_oficial": get_dolar_oficial(),
        "inflacion_mensual_oficial": get_inflacion_mensual_oficial()
    }

    # Guardar los datos en archivos CSV en la carpeta /temp colocandole el nombre de las claves como nombre del archivo y las claves como nombre de las columnas y los valores como los datos, por ejemplo:
    # dolar_blue.csv
    # tendriamos que tener un archivo con el siguiente formato:
    # fecha;[nombre de la variable, por ejemplo: dolar_blue, dolar_oficial, inflacion_mensual_oficial]
    # 2024-01-01;100
    # 2024-01-02;101
    # 2024-01-03;102
    # y asi sucesivamente

    for key, value in data.items():
        with open(f'temp/{key}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['fecha', key])
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and 'fecha' in item and 'valor' in item:
                        writer.writerow([item['fecha'], item['valor']])  # Escribir datos
                    else:
                        print_console("warning", f"Advertencia: Elemento de la lista no tiene el formato esperado para la clave {key}")
            else:
                # Manejo del caso cuando 'value' no es una lista
                print_console("warning", f"Advertencia: Se esperaba una lista pero se obtuvo {type(value)} para la clave {key}")

