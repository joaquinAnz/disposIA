import numpy as np

def dtw_distance(x, y):
    x = np.array(x)
    y = np.array(y)

    n = len(x)
    m = len(y)

    # matriz DTW
    dtw = np.full((n + 1, m + 1), np.inf)
    dtw[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(x[i - 1] - y[j - 1])
            dtw[i, j] = cost + min(
                dtw[i - 1, j],      # inserción
                dtw[i, j - 1],      # eliminación
                dtw[i - 1, j - 1]   # match
            )

    return dtw[n, m]
