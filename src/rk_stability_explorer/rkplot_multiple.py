
import matplotlib.pyplot as plt
import numpy as np


def make_grid(xmin=-8, xmax=2, ymin=-5.5, ymax=5.5, n=200):
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    return np.meshgrid(x, y)


    

def rkplot_multiple_ref(method_results, cols=2, cmap = "twilight"):
    import matplotlib.pyplot as plt
    import numpy as np

    n = len(method_results)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(2.8 * cols, 3.2*rows),
        sharex=True,
        sharey=True
    )

    axes = np.array(axes).reshape(-1)

    for ax, (X, Y, R, title) in zip(axes, method_results):
        levels = np.linspace(0, 2, 150)
        stable = np.abs(R) <= 1

        ax.contourf(X, Y, np.abs(R), levels=levels, cmap=cmap)
        ax.contour(X, Y, np.abs(R), levels=[1], colors="red", linewidths=2)
        ax.set_title(title, fontsize=12,fontweight="bold")

    for ax in axes[n:]:
        ax.remove()

    plt.tight_layout()
    return fig


def rkplot_multiple(method_results, cols=2, cmap="twilight"):
    import matplotlib.pyplot as plt
    import numpy as np

    n = len(method_results)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(2.8 * cols, 3.2 * rows),
        sharex=True,
        sharey=True
    )

    axes = np.array(axes).reshape(-1)

    for i, (ax, (X, Y, R, title)) in enumerate(zip(axes, method_results)):
        levels = np.linspace(0, 2, 150)

        ax.contourf(X, Y, np.abs(R), levels=levels, cmap=cmap)
        ax.contour(X, Y, np.abs(R), levels=[1], colors="red", linewidths=2)

        ax.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.6)

        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.tick_params(labelsize=8)
        # --- вычисляем позицию ---
        row = i // cols
        col = i % cols

        # --- подписи осей ---
        if col == 0:
            ax.set_ylabel("Im(z)", fontsize=10)
        else:
            ax.set_ylabel("")

        if row == rows - 1:
            ax.set_xlabel("Re(z)", fontsize=10)
        else:
            ax.set_xlabel("")

    # удалить лишние оси
    for ax in axes[n:]:
        ax.remove()

    plt.tight_layout()
    return fig