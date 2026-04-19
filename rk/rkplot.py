#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:14:49 2026

@author: hardware-numerics
"""

import matplotlib.pyplot as plt
import numpy as np


def make_grid(xmin=-4, xmax=2, ymin=-6, ymax=6, n=200):
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    return np.meshgrid(x, y)


def plot_stability(X, Y, R, title="Stability region"):
    plt.figure(figsize=(8, 6))

    levels = np.linspace(0, 2, 200)

    plt.contourf(X, Y, R, levels=levels, cmap="viridis")
    plt.contour(X, Y, R, levels=[1], colors="red", linewidths=2)

    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)

    plt.gca().set_aspect("equal")
    plt.title(title)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")

    #plt.colorbar()
