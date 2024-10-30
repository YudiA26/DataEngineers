import pandas as pd

# Ruta de entrada y salida
input_path = "./data/shows_january_2024.parquet"
output_path = "./data/shows_january_2024_cleaned.parquet"

# Cargar datos desde el archivo Parquet
df = pd.read_parquet(input_path)

# Imprimir los nombres de las columnas para inspección
print("Columnas en el DataFrame:", df.columns)

# ---- Paso 1: Eliminar Variables con Alta Correlación y Baja Cobertura ----
columns_to_drop = [
    '_embedded_show_network', '_embedded_show_dvdCountry', 'image',
    '_embedded_show_image', '_embedded_show_network_id',
    '_embedded_show_network_name', '_embedded_show_network_country_name',
    '_embedded_show_network_country_code', '_embedded_show_network_country_timezone',
    '_embedded_show_network_officialSite', '_embedded_show_webChannel',
    '_embedded_show_webChannel_country', 'image_medium', 'image_original'
]

# Eliminar columnas solo si existen en el DataFrame
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# ---- Paso 2: Imputación de Datos Faltantes ----
if 'runtime' in df.columns:
    df['runtime'].fillna(df['runtime'].median(), inplace=True)
if '_embedded_show_language' in df.columns:
    df['_embedded_show_language'].fillna(df['_embedded_show_language'].mode()[0], inplace=True)

# ---- Paso 3: Tratamiento de Outliers ----
if 'runtime' in df.columns:
    Q1 = df['runtime'].quantile(0.25)
    Q3 = df['runtime'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df['runtime'] = df['runtime'].clip(lower=lower_bound, upper=upper_bound)

# ---- Guardar el dataset limpio ----
df.to_parquet(output_path, compression='snappy')
print(f"Dataset limpio guardado en: {output_path}")
