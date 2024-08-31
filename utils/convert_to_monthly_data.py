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

def convert_to_monthly_data(root_path):
    if not os.path.exists(root_path):
        return 404  # Not Found

    try:
        for file_name in os.listdir(root_path):
            file_path = os.path.join(root_path, file_name)
            
            if os.path.isdir(file_path):
                continue  # Ignorar carpetas

            if not file_name.endswith('.csv'):
                return 403  # Forbidden

            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                return 500  # Internal Server Error

            if 'fecha' not in df.columns:
                return 400  # Bad Request

            # Agrupar por mes y guardar solo el último día de cada mes
            df['fecha'] = pd.to_datetime(df['fecha'])
            df = df.set_index('fecha').resample('M').last().reset_index()
            preprocessed_path = os.path.join(root_path, 'preprocessed')
            os.makedirs(preprocessed_path, exist_ok=True)
            df.to_csv(os.path.join(preprocessed_path, file_name), index=False)

        return 200  # OK
    except Exception as e:
        return 500  # Internal Server Error