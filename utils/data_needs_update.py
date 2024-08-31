import os
from datetime import datetime
from utils.print_console import print_console

def data_needs_update(temp_path):
    """
    Verifica la carpeta temp existe, si no existe la crea y retorna True, indicando que los datos necesitan ser actualizados.
    Si existe, verifica si contiene archivos, si no contiene archivos, retorna True, indicando que los datos necesitan ser actualizados.
    Si contiene archivos, verifica si alguno de ellos tiene más de un día de antigüedad, si es así, retorna True, indicando que los datos necesitan ser actualizados.
    Si no, retorna False, indicando que los datos no necesitan ser actualizados.
    """
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
        print_console("info", "Carpeta 'temp' creada, los datos necesitan ser actualizados")
        return True
    
    files = os.listdir(temp_path)
    if not files:
        print_console("info", "La carpeta 'temp' está vacía, los datos necesitan ser actualizados")
        return True
    
    for file in files:
        file_path = os.path.join(temp_path, file)
        if os.path.isfile(file_path):
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            days_old = (datetime.now() - last_modified_date).days
            if days_old > 1:
                print_console("info", "Los datos necesitan ser actualizados. Última actualización: " + last_modified_date.strftime("%d/%m/%Y %H:%M:%S"))
                return True

    print_console("info", "Los datos no necesitan ser actualizados. Última actualización: " + last_modified_date.strftime("%d/%m/%Y %H:%M:%S"))
    return False