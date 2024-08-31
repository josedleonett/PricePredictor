from utils.data_needs_update import data_needs_update
from utils.verify_and_normalize_dates import verify_and_normalize_dates
from utils.normalize_dates import normalize_dates
from utils.update_data import update_data


# Verificar si los datos necesitan ser actualizados
if data_needs_update("temp/online"):
    update_data("temp/online")

# Verifica si las fechas esta normalizadas
verify_and_normalize_dates("temp")
verify_and_normalize_dates("temp/online")