import pandas as pd
import sqlite3
from urllib.parse import urlparse

# Ruta de los archivos y la base de datos
parquet_path = "./data/shows_january_2024_cleaned.parquet"
sqlite_db_path = "./db/shows_data.db"

# Leer el archivo parquet limpio
df = pd.read_parquet(parquet_path)

# Conectar a la base de datos SQLite (crea la base de datos si no existe)
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

# Crear la tabla en SQLite con una estructura definida
table_creation_query = """
CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY,
    url TEXT,
    name TEXT,
    season INTEGER,
    number INTEGER,
    type TEXT,
    airdate DATE,
    airtime TEXT,
    airstamp TIMESTAMP,
    runtime INTEGER,
    image TEXT,
    summary TEXT,
    rating_average REAL,
    _links_self_href TEXT,
    _links_show_href TEXT,
    _links_show_name TEXT,
    _embedded_show_id INTEGER,
    _embedded_show_url TEXT,
    _embedded_show_name TEXT,
    _embedded_show_type TEXT,
    _embedded_show_language TEXT,
    _embedded_show_genres TEXT,
    _embedded_show_status TEXT,
    _embedded_show_runtime INTEGER,
    _embedded_show_averageRuntime REAL,
    _embedded_show_premiered DATE,
    _embedded_show_ended DATE,
    _embedded_show_officialSite TEXT,
    _embedded_show_schedule_time TEXT,
    _embedded_show_schedule_days TEXT,
    _embedded_show_rating_average REAL,
    _embedded_show_weight INTEGER
);
"""
cursor.execute(table_creation_query)

# Almacenar los datos en la base de datos SQLite
df.to_sql('shows', conn, if_exists='replace', index=False)

# Operaciones de agregación

# a. Calcular runtime promedio
avg_runtime_query = """
SELECT AVG(_embedded_show_averageRuntime) as avg_runtime
FROM shows;
"""
avg_runtime = cursor.execute(avg_runtime_query).fetchone()[0]
print("Runtime promedio:", avg_runtime)

# b. Conteo de shows de tv por género
genre_count_query = """
SELECT _embedded_show_genres, COUNT(*) as count
FROM shows
GROUP BY _embedded_show_genres;
"""
genre_counts = pd.read_sql_query(genre_count_query, conn)
print("\nConteo de shows por género:\n", genre_counts)

# c. Listar dominios únicos del sitio oficial
df['_embedded_show_officialSite'] = df['_embedded_show_officialSite'].fillna('')
df['domain'] = df['_embedded_show_officialSite'].apply(lambda url: urlparse(url).netloc if url else None)
unique_domains = df['domain'].dropna().unique()
print("\nDominios únicos de los sitios oficiales:\n", unique_domains)

# Cerrar la conexión a la base de datos
conn.close()
