from eralchemy import render_er

# Define la ruta de la base de datos SQLite y la ruta de salida de la imagen
sqlite_db_path = "./db/shows_data.db"
output_image_path = "./model/shows_data_schema.png"

# Genera el diagrama ER a partir de la base de datos SQLite
render_er(f"sqlite:///{sqlite_db_path}", output_image_path)

print(f"Diagrama ER generado y guardado en: {output_image_path}")
