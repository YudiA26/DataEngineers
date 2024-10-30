import pandas as pd
import json
import os

# Define la ruta del archivo JSON y del archivo Parquet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(BASE_DIR, 'json', 'shows_january_2024.json')
output_path = os.path.join(BASE_DIR, 'data', 'shows_january_2024.parquet')

def load_json_to_dataframe(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extrae los campos principales del episodio y los detalles del show
    df = pd.json_normalize(data, sep='_', 
                           meta=[
                               "id", "url", "name", "season", "number", "type", 
                               "airdate", "airstamp", "runtime", 
                               ["rating", "average"],
                               ["_embedded", "show", "id"],
                               ["_embedded", "show", "name"],
                               ["_embedded", "show", "type"],
                               ["_embedded", "show", "language"],
                               ["_embedded", "show", "genres"],
                               ["_embedded", "show", "status"],
                               ["_embedded", "show", "averageRuntime"],
                               ["_embedded", "show", "premiered"],
                               ["_embedded", "show", "ended"],
                               ["_embedded", "show", "officialSite"],
                               ["_embedded", "show", "webChannel", "name"]
                           ],
                           errors='ignore')
    
    # Análisis breve de las variables
    print("Tipos de datos de cada columna:")
    print(df.dtypes)
    print("\nConteo de valores nulos:")
    print(df.isnull().sum())
    print("\nValores únicos por columna:")
    
    for column in df.columns:
        # Convertir columnas que contengan listas a cadenas para evitar el error
        if df[column].apply(lambda x: isinstance(x, list)).any():
            df[column] = df[column].astype(str)
        
        unique_values = df[column].nunique()
        print(f"{column}: {unique_values} valores únicos")
    
    # ---- Paso 2: Convertir Variables No Soportadas ----
    # Convertir '_embedded_show_genres' y '_embedded_show_image' a texto si existen
    if '_embedded_show_genres' in df.columns:
        df['_embedded_show_genres'] = df['_embedded_show_genres'].astype(str)
    if '_embedded_show_image' in df.columns:
        df['_embedded_show_image'] = df['_embedded_show_image'].astype(str)
    
    return df

def save_to_parquet(df, file_path):
    df.to_parquet(file_path, compression='snappy')
    print(f"Datos guardados en {file_path}")

if __name__ == "__main__":
    # Cargar el JSON, procesarlo a un DataFrame y guardarlo como Parquet
    df = load_json_to_dataframe(input_path)
    save_to_parquet(df, output_path)
