
import matplotlib.pyplot as plt
import numpy as np


def make_grid(xmin=-4, xmax=2, ymin=-6, ymax=6, n=200):
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    return np.meshgrid(x, y)


def rkplot_multiple_old(method_results, cols=2):
    """
    method_results: list of tuples (X, Y, R, title)
    """
    n = len(method_results)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))

    axes = np.array(axes).reshape(-1)

    for ax, (X, Y, R, title) in zip(axes, method_results):
        levels = np.linspace(0, 2, 150)

        cf = ax.contourf(X, Y, R, levels=levels, cmap="flag")
        ax.contour(X, Y, R, levels=[1], colors="red", linewidths=1.5)

        ax.axhline(0, color="black", lw=0.5)
        ax.axvline(0, color="black", lw=0.5)

        ax.set_aspect("equal")
        ax.set_title(title)

    # убрать пустые оси
    for i in range(len(method_results), len(axes)):
        axes[i].axis("off")

    #plt.tight_layout()
    plt.tight_layout(pad=0.5, w_pad=0.3, h_pad=0.3)
    
    
def rkplot_multiple_1(method_results, cols=2):
    import matplotlib.pyplot as plt
    import numpy as np

    n = len(method_results)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(4.5 * cols, 4 * rows))

    axes = np.array(axes).reshape(-1)

    for ax, (X, Y, R, title) in zip(axes, method_results):
        levels = np.linspace(0, 2, 150)

        ax.contourf(X, Y, R, levels=levels, cmap="viridis")
        ax.contour(X, Y, R, levels=[1], colors="red", linewidths=1.5)

        ax.axhline(0, color="black", lw=0.5)
        ax.axvline(0, color="black", lw=0.5)

        ax.set_aspect("equal")
        #ax.set_title(title, fontsize=10)
        ax.set_title(title, fontsize=9, pad=2)

        # убираем лишний шум
        ax.set_xticks([])
        ax.set_yticks([])

    # убрать пустые
    for i in range(len(method_results), len(axes)):
        axes[i].axis("off")

    fig.subplots_adjust(
        left=0.05,
        right=0.98,
        top=0.92,
        bottom=0.05,
        wspace=0.05,
        hspace=0.18
    )

    plt.show()
    
    
def rkplot_multiple(method_results, cols=2):
    import matplotlib.pyplot as plt
    import numpy as np

    n = len(method_results)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(4.5 * cols, 4 * rows),
        sharex=True,
        sharey=True
    )

    axes = np.array(axes).reshape(-1)

    for idx, (ax, (X, Y, R, title)) in enumerate(zip(axes, method_results)):
        levels = np.linspace(0, 2, 150)
        stable = R <= 1
        ax.contourf(X, Y, R, levels=levels, cmap="twilight")
        ax.contour(X, Y, R, levels=[1], colors="red", linewidths=1.5)
        ax.contourf(X, Y, stable, levels=[0, 0.5, 1], colors=["white", "blue"], alpha=0.3)
        ax.contour(X, Y, R, levels=[1], colors="red", linewidths=2)

        ax.axhline(0, color="black", lw=0.5)
        ax.axvline(0, color="black", lw=0.5)

        ax.set_aspect("equal")
        ax.set_title(title, fontsize=9, pad=2)

        # оси только по краям
        if idx // cols == rows - 1:
            ax.set_xlabel("Re(z)")
        else:
            ax.set_xticks([])

        if idx % cols == 0:
            ax.set_ylabel("Im(z)")
        else:
            ax.set_yticks([])

        ax.set_xlim(X.min(), X.max())
        ax.set_ylim(Y.min(), Y.max())

    # удалить пустые
    for i in range(len(method_results), len(axes)):
        axes[i].axis("off")

    fig.subplots_adjust(
        left=0.07,
        right=0.98,
        top=0.92,
        bottom=0.08,
        wspace=0.05,
        hspace=0.08
    )

    plt.show()
