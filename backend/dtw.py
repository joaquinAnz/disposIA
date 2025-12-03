import numpy as np

def dtw_distance(x, y):
    x = np.array(x)
    y = np.array(y)

    n, m = len(x), len(y)
    dtw = np.full((n + 1, m + 1), np.inf)
    dtw[0, 0] = 0

    # Limitamos la ventana de comparación (10%) para evitar deformaciones
    w = abs(n - m) + int(0.1 * max(n, m))

    for i in range(1, n + 1):
        start = max(1, i - w)
        end = min(m + 1, i + w)

        for j in range(start, end):
            cost = abs(x[i - 1] - y[j - 1])
            dtw[i, j] = cost + min(
                dtw[i - 1, j],      # inserción
                dtw[i, j - 1],      # eliminación
                dtw[i - 1, j - 1]   # match
            )

    return float(dtw[n, m])
