# Recibe un root_path y verifica si todos los archivos CSV en el directorio tienen la columna 'fecha',
# Agrupa los datos por mes guardando un nuevo archivo en /preprocessed dejando solo el ultimo dia de cada mes. Por ejemplo:
# fecha;dolar_blue
# 2000-05-30;1.0
# 2000-05-31;1.5
# 2000-06-01;1.0
# 2000-06-02;1.0
# 2000-06-29;1.0
# 2000-06-30;1.2
# 2000-07-03;1.0
# 2000-07-04;1.0
# 2000-07-28;1.0
# 2000-07-31;1.8
# 2000-08-01;1.0
# 2000-08-02;1.0
# 2000-08-11;1.0
# 2000-08-14;1.0
# 2000-08-15;1.0
# 2000-08-31;1.9
# 2000-09-12;1.0
# 2000-09-22;1.7
# dejando solo:
# fecha;dolar_blue
# 2000-05-31;1.5
# 2000-06-30;1.2
# 2000-07-31;1.8
# 2000-08-31;1.9
# 2000-09-22;1.7
# Si no cumple con alguno de estos requisitos, muestra un mensaje de error.
# tabla de respuesta al estilo http status code:
# 200: ok si los datos cumplen con los requisitos
# 404: not found si el directorio no existe
# 500: internal server error si error al leer el archivo
# 403: forbidden - El archivo no es un CSV
# 400: bad request - El archivo no tiene la columna 'fecha'
# 406: not acceptable - El formato de la fecha no es YYYY-MM-DD

import os
import pandas as pd

from utils.print_console import print_console

def convert_to_monthly_data(input_path, output_path):
    if not os.path.exists(input_path):
        print_console("error", f"No se encuentra el directorio especificado: {input_path}")
        return 404

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    try:
        total_files = 0
        processed_files = 0
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            
            if os.path.isdir(file_path):
                continue

            total_files += 1

            if not file_name.endswith('.csv'):
                print_console("warning", f"El archivo {file_name} no es un CSV. Se omitirá.")
                continue

            try:
                df = pd.read_csv(file_path, delimiter=';')
            except Exception as e:
                print_console("error", f"Error al leer el archivo {file_name}: {e}")
                continue

            if 'fecha' not in df.columns:
                print_console("error", f"El archivo {file_name} no tiene la columna 'fecha'. Se omitirá.")
                continue

            try:
                df['fecha'] = pd.to_datetime(df['fecha'])
                df = df.set_index('fecha').resample('ME').last().reset_index()
                df.to_csv(os.path.join(output_path, file_name), index=False)
                processed_files += 1
                print_console("", f"El archivo {file_name} se ha convertido a datos mensuales.")
            except Exception as e:
                print_console("error", f"Error al pre-procesar el archivo {file_name}: {e}")

        print_console("success", f"Se han pre-procesado {processed_files} de {total_files} archivos en {input_path}.")
        return 200 if processed_files > 0 else 400
    except Exception as e:
        print_console("error", f"Error al convertir los archivos a datos mensuales: {e}")
        return 500