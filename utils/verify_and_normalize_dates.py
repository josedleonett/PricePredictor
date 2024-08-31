import os
import pandas as pd
from utils.print_console import print_console

def verify_and_normalize_dates(root_path):
    """
    Funcion para verificar si las fechas necesitan ser normalizadas
    Recibe un root_path y verifica si todos los archivos CSV en el directorio tienen la columna 'fecha'.
    Luego verifica celda por celda si el formato de la fecha es YYYY-MM-DD, si no lo es, muestra un mensaje de advertencia y se corrige. Despues de corregir, muestra un mensaje de exito.
    tabla de respuesta al estilo http status code:
    200: ok si las fechas no necesitan ser normalizadas
    404: not found si el directorio no existe
    500: internal server error si error al leer el archivo
    403: forbidden - El archivo no es un CSV
    400: bad request - El archivo no tiene la columna 'fecha'
    406: not acceptable - El formato de la fecha no es YYYY-MM-DD
    """
    print_console("", "Verificando si las fechas están normalizadas")

    if not os.path.exists(root_path):
        print_console("error", f"No se encuentra el directorio especificado {root_path}")
        return 404

    errors = []

    for file_name in os.listdir(root_path):
        file_path = os.path.join(root_path, file_name)
        if not file_name.endswith('.csv'):
            print_console("error", f"El archivo {file_name} no es un CSV")
            errors.append(403)
            continue

        try:
            df = pd.read_csv(file_path, delimiter=';')
        except Exception as e:
            print_console("error", f"Error al leer el archivo {file_name}: {e}")
            errors.append(500)
            continue

        if 'fecha' not in df.columns:
            print_console("error", f"El archivo {file_name} no tiene la columna 'fecha'")
            errors.append(400)
            continue

        def is_valid_date(date_str):
            try:
                pd.to_datetime(date_str, format='%Y-%m-%d')
                return True
            except ValueError:
                return False

        incorrect_dates = df[~df['fecha'].apply(is_valid_date)]

        # Si hay fechas en formato incorrecto, se corrige
        if not incorrect_dates.empty:
            print_console("warning", f"El archivo {file_name} tiene {len(incorrect_dates)} fechas en formato incorrecto. Corrigiendo...")

            corrected_count = 0
            for i, date in incorrect_dates.iterrows():
                try:
                    corrected_date = pd.to_datetime(date['fecha'], errors='coerce').strftime('%Y-%m-%d')
                    if pd.notna(corrected_date):
                        df.at[i, 'fecha'] = corrected_date
                        corrected_count += 1
                        print_console("info", f"Fecha corregida en fila {i}: {date['fecha']} -> {corrected_date}")
                    else:
                        print_console("error", f"No se pudo corregir la fecha en fila {i}: {date['fecha']}")
                except Exception as e:
                    print_console("error", f"Error al corregir la fecha en fila {i}: {date['fecha']} - {e}")

            # Guardar el DataFrame corregido en el archivo CSV
            df.to_csv(file_path, index=False, sep=';')

            if df[~df['fecha'].apply(is_valid_date)].empty:
                print_console("success", f"Se han corregido {corrected_count} fechas en el archivo {file_name}")
            else:
                remaining_incorrect = len(df[~df['fecha'].apply(is_valid_date)])
                print_console("error", f"El archivo {file_name} tiene {remaining_incorrect} fechas que no se pudieron corregir")
                errors.append(406)

    if not errors:
        print_console("success", "Las fechas están normalizadas")
        return 200
    else:
        return max(errors)