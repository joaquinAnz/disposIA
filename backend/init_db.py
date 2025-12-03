import sqlite3

conn = sqlite3.connect("songs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS canciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    artista TEXT NOT NULL,
    melodia_path TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente.")
