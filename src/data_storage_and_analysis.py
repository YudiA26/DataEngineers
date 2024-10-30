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

# Crear tablas de dimensiones y de hechos
# Dimensión Show
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_show (
    show_id INTEGER PRIMARY KEY,
    show_name TEXT,
    show_type TEXT,
    show_language TEXT,
    show_status TEXT,
    show_runtime INTEGER,
    show_averageRuntime REAL,
    show_premiered DATE,
    show_ended DATE,
    show_officialSite TEXT,
    show_weight INTEGER
);
""")

# Dimensión Género
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT UNIQUE
);
""")

# Dimensión Horario
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_time TEXT,
    schedule_days TEXT
);
""")

# Tabla de Hechos: Episodios
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_episode (
    episode_id INTEGER PRIMARY KEY,
    show_id INTEGER,
    season INTEGER,
    number INTEGER,
    airdate DATE,
    airtime TEXT,
    airstamp TIMESTAMP,
    runtime INTEGER,
    rating_average REAL,
    summary TEXT,
    genre_id INTEGER,
    schedule_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES dim_show(show_id),
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id),
    FOREIGN KEY (schedule_id) REFERENCES dim_schedule(schedule_id)
);
""")

# Poblar tablas de dimensiones y de hechos
# Dimensión Show
dim_show_df = df[[
    '_embedded_show_id', '_embedded_show_name', '_embedded_show_type',
    '_embedded_show_language', '_embedded_show_status', '_embedded_show_runtime',
    '_embedded_show_averageRuntime', '_embedded_show_premiered',
    '_embedded_show_ended', '_embedded_show_officialSite', '_embedded_show_weight'
]].drop_duplicates().rename(columns={
    '_embedded_show_id': 'show_id',
    '_embedded_show_name': 'show_name',
    '_embedded_show_type': 'show_type',
    '_embedded_show_language': 'show_language',
    '_embedded_show_status': 'show_status',
    '_embedded_show_runtime': 'show_runtime',
    '_embedded_show_averageRuntime': 'show_averageRuntime',
    '_embedded_show_premiered': 'show_premiered',
    '_embedded_show_ended': 'show_ended',
    '_embedded_show_officialSite': 'show_officialSite',
    '_embedded_show_weight': 'show_weight'
})
dim_show_df.to_sql('dim_show', conn, if_exists='replace', index=False)

# Dimensión Género
genres = df['_embedded_show_genres'].explode().dropna().unique()
dim_genre_df = pd.DataFrame(genres, columns=['genre_name']).reset_index().rename(columns={'index': 'genre_id'})
dim_genre_df.to_sql('dim_genre', conn, if_exists='replace', index=False)

# Dimensión Horario
dim_schedule_df = df[['_embedded_show_schedule_time', '_embedded_show_schedule_days']].drop_duplicates().rename(
    columns={
        '_embedded_show_schedule_time': 'schedule_time',
        '_embedded_show_schedule_days': 'schedule_days'
    }
)
dim_schedule_df.to_sql('dim_schedule', conn, if_exists='replace', index=False)

# Poblar Tabla de Hechos
# Asignar ID de género y horario a cada episodio
df = df.merge(dim_genre_df, how='left', left_on='_embedded_show_genres', right_on='genre_name')
df = df.merge(dim_schedule_df.reset_index().rename(columns={'index': 'schedule_id'}), how='left',
              left_on=['_embedded_show_schedule_time', '_embedded_show_schedule_days'],
              right_on=['schedule_time', 'schedule_days'])

# Crear la tabla de hechos fact_episode
fact_episode_df = df[[
    'id', '_embedded_show_id', 'season', 'number', 'airdate', 'airtime', 'airstamp', 'runtime',
    'rating_average', 'summary', 'genre_id', 'schedule_id'
]].rename(columns={'id': 'episode_id', '_embedded_show_id': 'show_id'})

fact_episode_df.to_sql('fact_episode', conn, if_exists='replace', index=False)

# a. Calcular runtime promedio de shows
avg_runtime_query = """
SELECT AVG(show_averageRuntime) as avg_runtime
FROM dim_show;
"""
avg_runtime = cursor.execute(avg_runtime_query).fetchone()[0]
print("Runtime promedio de shows:", avg_runtime)

# b. Conteo de shows de tv por género
genre_count_query = """
SELECT g.genre_name, COUNT(*) as count
FROM fact_episode e
JOIN dim_genre g ON e.genre_id = g.genre_id
GROUP BY g.genre_name;
"""
genre_counts = pd.read_sql_query(genre_count_query, conn)
print("\nConteo de shows por género:\n", genre_counts)

# c. Listar dominios únicos del sitio oficial
dim_show_df['domain'] = dim_show_df['show_officialSite'].fillna('').apply(lambda url: urlparse(url).netloc if url else None)
unique_domains = dim_show_df['domain'].dropna().unique()
print("\nDominios únicos de los sitios oficiales:\n", unique_domains)

# Cerrar la conexión a la base de datos
conn.close()
