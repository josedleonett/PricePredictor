import os
import pandas as pd
from datetime import datetime


def normalize_dates(root_path):
    # Verificar que el directorio existe
    if not os.path.isdir(root_path):
        print("El directorio especificado no existe.")
        return

    # Iterar sobre todos los archivos en el directorio
    for filename in os.listdir(root_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(root_path, filename)
            try:
                # Leer el archivo CSV
                df = pd.read_csv(file_path, delimiter=';')

                # Verificar que el archivo tiene la columna 'fecha'
                if 'fecha' not in df.columns:
                    print(f"El archivo {filename} no contiene la columna 'fecha'.")
                    continue

                # Convertir la columna 'fecha' al formato '%Y-%m-%d'
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')

                # Guardar el archivo CSV con las fechas normalizadas
                df.to_csv(file_path, index=False, sep=';')
                print(f"Fechas normalizadas en '{filename}'.")

            except Exception as e:
                print(f"Error al procesar el archivo {filename}: {e}")
