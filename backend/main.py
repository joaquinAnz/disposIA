from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import numpy as np
from pitch_extractor import extract_pitch
from dtw import dtw_distance
import os

app = FastAPI()

# Habilitar CORS para que Swagger funcione bien
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "songs.db"
MELODY_DIR = "melodias"

# Crear DB si no existe
conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    artist TEXT,
    melody_path TEXT
)
""")
conn.commit()
conn.close()


# ==========================================
#   ENDPOINT: Registrar canción con audio
# ==========================================
@app.post("/registrar")
async def registrar_cancion(
    title: str,
    artist: str,
    file: UploadFile = File(...)
):
    audio_bytes = await file.read()

    # Extraer la melodía del archivo subido
    melody = extract_pitch(audio_bytes)
    if melody is None or len(melody) == 0:
        return {"error": "No se pudo extraer la melodía del audio"}

    # Crear carpeta si no existe
    os.makedirs(MELODY_DIR, exist_ok=True)

    # Nombre del archivo .npy donde se guardará la melodía
    melody_filename = f"{title}_{artist}.npy".replace(" ", "_")
    melody_path = os.path.join(MELODY_DIR, melody_filename)

    # Guardar el array de pitch
    np.save(melody_path, melody)

    # Registrar en DB
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO songs (title, artist, melody_path) VALUES (?, ?, ?)",
        (title, artist, melody_filename)
    )
    conn.commit()
    conn.close()

    return {
        "mensaje": "Canción registrada correctamente",
        "title": title,
        "artist": artist,
        "archivo_melodia": melody_filename
    }


# ==========================================
#   ENDPOINT: Buscar canción por similitud
# ==========================================
@app.post("/buscar")
async def buscar_cancion(file: UploadFile = File(...)):
    # Leer archivo subido
    audio_bytes = await file.read()

    # Extraer melodia del audio de entrada
    input_melody = extract_pitch(audio_bytes)
    if input_melody is None or len(input_melody) == 0:
        return {"error": "No se pudo extraer la melodía del audio de entrada"}

    # Leer canciones registradas en la DB
    conn = sqlite3.connect(DB)
    songs = conn.execute("SELECT id, title, artist, melody_path FROM songs").fetchall()
    conn.close()

    if len(songs) == 0:
        return {"error": "No hay canciones registradas en la base de datos"}

    best_match = None
    best_distance = float("inf")

    # Comparar DTW con cada canción
    for song_id, title, artist, melody_path in songs:
        full_path = os.path.join(MELODY_DIR, melody_path)

        # Verificar que exista el archivo .npy
        if not os.path.exists(full_path):
            continue

        # Cargar melodía registrada
        ref_melody = np.load(full_path, allow_pickle=True)

        # Calcular distancia DTW
        distance = dtw_distance(input_melody, ref_melody)

        # Buscar el mínimo
        if distance < best_distance:
            best_distance = distance
            best_match = {
                "id": song_id,
                "title": title,
                "artist": artist,
                "distance": float(distance)
            }

    if best_match is None:
        return {"error": "No se encontró coincidencia"}

    return {
        "mensaje": "Canción más parecida encontrada",
        "resultado": best_match
    }
