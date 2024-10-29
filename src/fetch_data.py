import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = "http://api.tvmaze.com/schedule/web?date="

# Imprime el directorio actual para verificar desde dónde se ejecuta
print("Directorio actual:", os.getcwd())

# Ajusta la ruta según el directorio actual
if os.path.basename(os.getcwd()) == "src":
    output_path = '../json/shows_january_2024.json'
else:
    output_path = './json/shows_january_2024.json'

def fetch_shows_data():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    all_shows = []

    while start_date <= end_date:
        date_str = start_date.strftime('%Y-%m-%d')
        response = requests.get(f"{BASE_URL}{date_str}")
        if response.status_code == 200:
            all_shows.extend(response.json())
        start_date += timedelta(days=1)

    with open(output_path, 'w') as f:
        json.dump(all_shows, f, indent=4)

    print(f"Datos guardados en {output_path}")

if __name__ == "__main__":
    fetch_shows_data()
