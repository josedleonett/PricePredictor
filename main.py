from utils.data_needs_update import data_needs_update
from utils.update_data import update_data


# Verificar si los datos necesitan ser actualizados
if data_needs_update():
    update_data()