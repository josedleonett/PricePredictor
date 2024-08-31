# Funcion para verificar si las fechas necesitan ser normalizadas
# Recibe un root_path y verifica si todos los archivos CSV en el directorio tienen la columna 'fecha' con el formato YYYY-MM-DD, si encuentra un archivo que no cumple con el formato, retorna True, si no encuentra ninguno, retorna False 

import os
import pandas as pd
from utils.print_console import print_console

def dates_needs_normalization(root_path):
    # Verificar que el directorio existe
    if not os.path.isdir(root_path):
        print_console("error", "El directorio especificado no existe.")
        return False
    
    # Iterar sobre todos los archivos en el directorio
    for filename in os.listdir(root_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(root_path, filename)
            try:
                # Leer el archivo CSV
                df = pd.read_csv(file_path, delimiter=';')
                
                # Verificar que el archivo tiene la columna 'fecha'
                if 'fecha' not in df.columns:
                    print_console("error", f"El archivo {filename} no contiene la columna 'fecha'.")
                    return False
                
                # Verificar que la columna 'fecha' tiene el formato YYYY-MM-DD
                if not df['fecha'].apply(lambda x: isinstance(x, str) and len(x) == 10 and x.count('-') == 2 and x.index('-') == 4 and x.rindex('-') == 7):
                    print_console("error", f"El archivo {filename} no tiene el formato YYYY-MM-DD en la columna 'fecha'.")
                    return True
            except Exception as e:
                print_console("error", f"Error al leer el archivo {filename}: {e}")
                return True
    return False    