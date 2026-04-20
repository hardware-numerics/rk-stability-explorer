import numpy as np



def stability_function(z, A, b):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float).reshape(-1)  # (n,)

    n = A.shape[0]
    I = np.eye(n)
    ones = np.ones(n)

    result = np.zeros_like(z, dtype=float)

    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            M = I - z[i, j] * A  # (n, n)

            try:
                x = np.linalg.solve(M, ones)  # (n,)
            except np.linalg.LinAlgError:
                x = np.linalg.lstsq(M, ones, rcond=None)[0]

            # ВАЖНО: b^T x
            Rz = 1 + z[i, j] * (b @ x)

            result[i, j] = abs(Rz)

    return result