from pitch_extractor import extract_pitch

# Abre tu audio de prueba
with open("test.wav", "rb") as f:
    audio_bytes = f.read()

melody = extract_pitch(audio_bytes)

print("=== RESULTADO PYIN ===")
print("Puntos detectados:", len(melody))
print("Primeros 20 valores:", melody[:20])
