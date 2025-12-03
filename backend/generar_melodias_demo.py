import numpy as np
import os

os.makedirs("base_melodias", exist_ok=True)

# Melodía estilo pop (sube y baja suave)
pop = np.array([220, 230, 240, 250, 245, 238, 230, 225, 220, 215], dtype=np.float32)

# Melodía estilo rock (más agresiva, saltos grandes)
rock = np.array([110, 130, 150, 170, 160, 140, 120, 115, 110], dtype=np.float32)

# Balada suave (notas largas, cambios lentos)
balada = np.array([260, 262, 265, 268, 270, 268, 265, 262, 260], dtype=np.float32)

# Latina (patrón rítmico ascendente-descendente característico)
latina = np.array([200, 210, 220, 230, 225, 215, 205, 215, 225, 230, 220], dtype=np.float32)

# Electrónica (notas repetidas con saltos)
electro = np.array([300, 300, 305, 310, 310, 305, 300, 295, 295, 300], dtype=np.float32)

np.save("base_melodias/pop_demo.npy", pop)
np.save("base_melodias/rock_demo.npy", rock)
np.save("base_melodias/balada_demo.npy", balada)
np.save("base_melodias/latina_demo.npy", latina)
np.save("base_melodias/electro_demo.npy", electro)

print("¡Melodías demo generadas exitosamente!")
