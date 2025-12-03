import numpy as np
import librosa
import io

def extract_pitch(audio_bytes):
    try:
        # Cargar audio a 16 kHz mono
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)

        # Extraer pitch con pyin
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz('C2'),  # 65 Hz
            fmax=librosa.note_to_hz('C7'),  # 2093 Hz
            frame_length=1024,
            hop_length=256
        )

        # Convertir a array numpy
        f0 = np.array(f0)

        # Eliminar valores no vocalizados (None)
        f0_clean = f0[~np.isnan(f0)]

        # Devolver como lista
        return f0_clean.tolist()

    except Exception as e:
        print("ERROR:", e)
        return []
