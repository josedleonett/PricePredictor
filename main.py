from utils.data_needs_update import data_needs_update
from utils.update_data import update_data
from utils.verify_and_normalize_dates import verify_and_normalize_dates
from utils.convert_to_monthly_data import convert_to_monthly_data


# Verificar si los datos necesitan ser actualizados
if data_needs_update("temp/raw_data/online"):
    update_data("temp/raw_data/online")

# Verifica si las fechas esta normalizadas
verify_and_normalize_dates("temp/raw_data/online")
verify_and_normalize_dates("temp/raw_data/offline")

# Verifica y preprocesa los datos dejando solo los datos mensuales
convert_to_monthly_data("temp/raw_data/online", "temp/pre-processed")
convert_to_monthly_data("temp/raw_data/offline", "temp/pre-processed")