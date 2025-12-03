import numpy as np
from dtw import dtw

def comparar_melodias(query, database):
    mejor = None
    mejor_dist = float("inf")

    for nombre, melodia in database.items():
        dist = dtw(query, melodia).normalizedDistance

        if dist < mejor_dist:
            mejor_dist = dist
            mejor = nombre

    return mejor, mejor_dist
