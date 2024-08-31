import pandas as pd
import matplotlib.pyplot as plt

from utils.normalize_dates import normalize_dates
from utils.calculate_monthly_raw_data import calculate_monthly_raw_data
from request.get_inflacion_mensual_oficial import get_inflacion_mensual_oficial
from request.get_dolar_blue import get_dolar_blue
from request.get_dolar_oficial import get_dolar_oficial

# Normalizar las fechas (si es necesario)
normalize_dates("raw_data/time_series")
calculate_monthly_raw_data("raw_data/time_series")

# Cargar los datos desde archivos CSV con el delimitador correcto
precio_df = pd.read_csv('raw_data/time_series/precio_articulo.csv', delimiter=';', parse_dates=['fecha'], dayfirst=False)
inflacion_df = pd.read_csv(get_inflacion_mensual_oficial(), delimiter=';', parse_dates=['fecha'], dayfirst=False)
dolar_blue_df = pd.read_csv(get_dolar_blue(), delimiter=';', parse_dates=['fecha'], dayfirst=False)
dolar_oficial_df = pd.read_csv(get_dolar_oficial(), delimiter=';', parse_dates=['fecha'], dayfirst=False)

# Renombrar las columnas 'valor' para diferenciar cada DataFrame
precio_df.rename(columns={'valor': 'precio_articulo'}, inplace=True)
inflacion_df.rename(columns={'valor': 'inflacion'}, inplace=True)
dolar_blue_df.rename(columns={'valor': 'dolar_blue'}, inplace=True)
dolar_oficial_df.rename(columns={'valor': 'dolar_oficial'}, inplace=True)

# Revisar los primeros registros de los DataFrames
print(precio_df.head())
print(inflacion_df.head())
print(dolar_blue_df.head())
print(dolar_oficial_df.head())

# Unir los DataFrames por la columna 'fecha'
merged_df = precio_df.merge(inflacion_df, on='fecha') \
                     .merge(dolar_blue_df, on='fecha') \
                     .merge(dolar_oficial_df, on='fecha')

# Revisar los datos combinados
print(merged_df.head())


plt.figure(figsize=(14, 7))

# Plot de Precio del Artículo
plt.plot(merged_df['fecha'], merged_df['precio_articulo'], label='Precio del Artículo', color='blue')

# Plot de Inflación
plt.plot(merged_df['fecha'], merged_df['inflacion'], label='Inflación', color='red')

# Plot de Dólar Blue
plt.plot(merged_df['fecha'], merged_df['dolar_blue'], label='Dólar Blue', color='green')

# Plot de Dólar Oficial
plt.plot(merged_df['fecha'], merged_df['dolar_oficial'], label='Dólar Oficial', color='orange')

plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.title('Tendencias de Precio del Artículo, Inflación y Dólares')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

