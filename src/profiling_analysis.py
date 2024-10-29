import pandas as pd
from pandas_profiling import ProfileReport

# Ruta de entrada y salida
input_path = "./data/shows_january_2024.parquet"
output_path = "./profiling/shows_january_2024_profile.html"

# Cargar datos desde el archivo Parquet
df = pd.read_parquet(input_path)

# Generar el reporte de profiling
profile = ProfileReport(df, title="Shows January 2024 Profile Report", explorative=True)

# Guardar el reporte en HTML
profile.to_file(output_path)

print(f"El reporte de profiling ha sido guardado en: {output_path}")
