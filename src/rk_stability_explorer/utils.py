from importlib.resources import files
import numpy as np
from fractions import Fraction
from .butcher import load_method

_METHODS_CACHE = None

def _build_registry():
    base = files("rk_stability_explorer.methods")
    registry = {}

    for subdir in base.iterdir():
        if subdir.is_dir():
            for f in subdir.iterdir():
                if f.name.endswith(".yaml"):
                    registry[f.stem] = f

    return registry


def load_builtin(name: str):
    global _METHODS_CACHE

    if _METHODS_CACHE is None:
        _METHODS_CACHE = _build_registry()

    if name not in _METHODS_CACHE:
        raise ValueError(f"Unknown method: {name}")

    return load_method(_METHODS_CACHE[name])



def list_methods():
    base = files("rk_stability_explorer.methods")
    names = []

    for subdir in base.iterdir():
        if subdir.is_dir():
            for f in subdir.iterdir():
                if f.name.endswith(".yaml"):
                    names.append(f.stem)

    return sorted(names)


def list_methods_grouped():
    base = files("rk_stability_explorer.methods")
    result = {}

    for subdir in base.iterdir():
        if subdir.is_dir():
            result[subdir.name] = [
                f.stem for f in subdir.iterdir() if f.name.endswith(".yaml")
            ]

    return result


from fractions import Fraction

def format_number(x, tol=1e-10):
    if isinstance(x, str):
        return x

    frac = Fraction(x).limit_denominator(100)
    if abs(float(frac) - x) < tol:
        if frac.denominator == 1:
            return f"{frac.numerator}"
        return f"{frac.numerator}/{frac.denominator}"

    return f"{x:.3g}"


def print_butcher_table(method):
    from .utils import load_builtin

    if isinstance(method, str):
        method = load_builtin(method)

    name = method.get("name", "Unknown")
    A = method["A"]
    b = method["b"]
    c = method["c"]

    s = len(b)

    print(f"\nMethod: {name}\n")

    rows = []
    for i in range(s):
        row = [format_number(c[i])] + [
            format_number(A[i][j]) for j in range(s)
        ]
        rows.append(row)

    b_row = [""] + [format_number(x) for x in b]

    # ширины колонок
    cols = list(zip(*rows, b_row))
    col_widths = [max(len(str(x)) for x in col) for col in cols]

    # печать строк
    for row in rows:
        left = str(row[0]).rjust(col_widths[0])
        right = "  ".join(
            str(x).rjust(w) for x, w in zip(row[1:], col_widths[1:])
        )
        print(f"{left} │ {right}")

    # горизонтальная линия
    total_width = sum(col_widths) + 3 * len(col_widths)
    print("─" * total_width)

    # нижняя строка (b)
    left = "".rjust(col_widths[0])
    right = "  ".join(
        str(x).rjust(w) for x, w in zip(b_row[1:], col_widths[1:])
    )
    print(f"{left} │ {right}")