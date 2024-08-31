import os
import pandas as pd
from utils.print_console import print_console


def aggregate_monthly_data(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, delimiter=';')

        # Verificar que el archivo tiene las columnas necesarias
        if 'fecha' not in df.columns or 'valor' not in df.columns:
            print_console("error", f"El archivo {file_path} no contiene las columnas 'fecha' o 'valor'.")
            return

        # Convertir la columna 'fecha' a tipo datetime
        df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d', errors='coerce')

        # Verificar si se realizaron conversiones exitosas
        if df['fecha'].isnull().any():
            print_console("warning", f"Advertencia: Algunas fechas en {file_path} no pudieron ser convertidas.")
            df = df.dropna(subset=['fecha'])  # Eliminar filas con fechas inválidas

        # Extraer el año y el mes de la fecha
        df['año_mes'] = df['fecha'].dt.to_period('M')

        # Agrupar valores por mes y mantener solo el último día de cada mes
        monthly_data = df.sort_values('fecha').groupby('año_mes').tail(1).reset_index(drop=True)

        # imprimir la cantidad de items del dataframe
        print_console("info", f"Cantidad de items del dataframe: {len(monthly_data)}")

        # Redondear los valores a dos decimales
        monthly_data['valor'] = monthly_data['valor'].round(2)

        # Convertir 'año_mes' de nuevo a formato de fecha (primer día del mes siguiente)
        monthly_data['fecha'] = (monthly_data['año_mes'] + 1).dt.to_timestamp()
        monthly_data = monthly_data[['fecha', 'valor']]

        # Sobrescribir el archivo CSV con los datos agregados
        monthly_data.to_csv(file_path, index=False, sep=';')

        print_console("info", f"Datos mensuales agregados en '{file_path}'.")

    except Exception as e:
        print_console("error", f"Error al procesar el archivo {file_path}: {e}")


def calculate_monthly_raw_data(root_path):
    # Verificar que el directorio existe
    if not os.path.isdir(root_path):
        print_console("error", "El directorio especificado no existe.")
        return

    # Iterar sobre todos los archivos en el directorio
    for filename in os.listdir(root_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(root_path, filename)
            aggregate_monthly_data(file_path)


# # Llamar a la función con la ruta deseada
# calculate_average_monthly_raw_data("raw_data/time_series")
#
# # Ejemplo de carga y revisión de datos
# precio_df = pd.read_csv('raw_data/time_series/precio_articulo.csv', delimiter=';', parse_dates=['fecha'], dayfirst=False)
# inflacion_df = pd.read_csv('raw_data/time_series/inflacion_mensual_oficial.csv', delimiter=';', parse_dates=['fecha'], dayfirst=False)
# dolar_blue_df = pd.read_csv('raw_data/time_series/dolar_blue.csv', delimiter=';', parse_dates=['fecha'], dayfirst=False)
# dolar_oficial_df = pd.read_csv('raw_data/time_series/dolar_oficial.csv', delimiter=';', parse_dates=['fecha'], dayfirst=False)
# print(precio_df.head())
# print(inflacion_df.head())
# print(dolar_blue_df.head())
# print(dolar_oficial_df.head())
