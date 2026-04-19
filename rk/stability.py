#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:14:16 2026

@author: hardware-numerics
"""

import numpy as np


def stability_function(z, A, b):
    n = len(b)
    I = np.eye(n)
    ones = np.ones(n)

    result = np.zeros_like(z, dtype=float)

    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            zz = z[i, j]

            M1 = I - zz * A + zz * np.outer(ones, b)
            M2 = I - zz * A

            result[i, j] = abs(np.linalg.det(M1) / np.linalg.det(M2))

    return result


def stability_function_fast(z, A, b):
    """
    vectorized version
    z: complex grid (NxM)
    """

    A = np.asarray(A)
    b = np.asarray(b)

    n = len(b)
    I = np.eye(n)
    ones = np.ones(n)

    # (n,n)
    outer = np.outer(ones, b)

    # reshape для broadcasting
    Z = z[..., None, None]  # (Nx, Ny, 1, 1)

    M2 = I - Z * A
    M1 = M2 + Z * outer

    # считаем det по последним двум осям
    det1 = np.linalg.det(M1)
    det2 = np.linalg.det(M2)
    eps = 1e-14
    return np.abs(det1) / (np.abs(det2) + eps)



def stability_function_ultimate(z, A, b):
    """
    no det, but linear system:
    R(z) = |1 + z * b^T (I - zA)^(-1) 1|
    """

    A = np.asarray(A)
    b = np.asarray(b)

    n = len(b)
    I = np.eye(n)
    ones = np.ones(n)

    result = np.zeros_like(z, dtype=float)

    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            zz = z[i, j]

            M = I - zz * A

            # решаем (I - zA)x = 1
            x = np.linalg.solve(M, ones)

            Rz = 1 + zz * np.dot(b, x)

            result[i, j] = np.abs(Rz)

    return result


def stability_function_ultimate_fast(z, A, b):
    A = np.asarray(A)
    b = np.asarray(b)

    n = len(b)
    I = np.eye(n)
    ones = np.ones(n)

    result = np.zeros_like(z, dtype=float)

    for i in range(z.shape[0]):
        M = I - z[i, :, None, None] * A  # (Ny, n, n)
        
        try:
            x = np.linalg.solve(M, ones)
        except np.linalg.LinAlgError:
            x = np.linalg.lstsq(M, ones, rcond=None)[0]
    
        # решаем пачкой
        X = np.linalg.solve(M, ones)  # (Ny, n)

        Rz = 1 + z[i, :] * (X @ b)

        result[i, :] = np.abs(Rz)

    return result
