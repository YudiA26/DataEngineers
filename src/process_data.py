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
    return df

def save_to_parquet(df, file_path):
    df.to_parquet(file_path, compression='snappy')
    print(f"Datos guardados en {file_path}")

if __name__ == "__main__":
    # Cargar el JSON, procesarlo a un DataFrame y guardarlo como Parquet
    df = load_json_to_dataframe(input_path)
    save_to_parquet(df, output_path)
