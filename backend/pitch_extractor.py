import numpy as np
import librosa
import io
from scipy.signal import medfilt

def extract_pitch(audio_bytes):
    try:
        # Cargar audio
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)

        # Extraer pitch (pyin)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            frame_length=1024,
            hop_length=256
        )

        # Limpiar pitch
        f0 = np.array(f0)
        f0 = f0[~np.isnan(f0)]

        if len(f0) < 5:
            return []

        # 1) Suavizar ruidos (filtro de mediana)
        f0 = medfilt(f0, kernel_size=5)

        # 2) Normalización
        f0 = (f0 - np.mean(f0)) / np.std(f0)

        return f0.tolist()

    except Exception as e:
        print("ERROR:", e)
        return []
