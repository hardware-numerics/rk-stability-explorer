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


#-------detect where precision is needed----
from fractions import Fraction

def detect_method_type(method):
    b = method["b"]
    A = method["A"]
    s = len(b)

    max_den = 1

    for row in A:
        for x in row:
            if isinstance(x, Fraction):
                max_den = max(max_den, x.denominator)

    if s == 4:
        return "RK4"

    if s >= 10 or max_den > 1000:
        return "DOP_LIKE"

    return "RK_SMALL"

#def format_number(x, method_type="AUTO"):
#    if isinstance(x, str):
#        return x
#
#    frac = Fraction(x) if not isinstance(x, Fraction) else x
#
#    if method_type == "DOP_LIKE":
#        # точный режим
#        f = frac
#    else:
#        # красивый режим
#        f = frac.limit_denominator(20)
#
#    if f.denominator == 1:
#        return str(f.numerator)
#
#    return f"{f.numerator}/{f.denominator}"



#def format_number(x, method_type="AUTO"):
#    # строки оставляем как есть
#    if isinstance(x, str):
#        return x
#
#    # --- CASE 1: Fraction (точные методы) ---
#    if isinstance(x, Fraction):
#        if method_type == "DOP_LIKE":
#            f = x  # без упрощения
#        else:
#            f = x.limit_denominator(20)
#
#        if f.denominator == 1:
#            return str(f.numerator)
#
#        return f"{f.numerator}/{f.denominator}"
#
#    # --- CASE 2: float (численные методы) ---
#    if isinstance(x, float):
#        # аккуратный вывод без мусора
#        return f"{x:.6g}"
#
#    # fallback
#    return str(x)

def format_number(x, method_type="AUTO"):
    if isinstance(x, str):
        return x

    # --- Fraction ---
    if isinstance(x, Fraction):
        if method_type == "DOP_LIKE":
            f = x
        else:
            f = x.limit_denominator(20)

        if f.denominator == 1:
            return str(f.numerator)

        return f"{f.numerator}/{f.denominator}"

    # --- float ---
    if isinstance(x, float):
        # попытка распознать простую дробь
        frac = Fraction(x).limit_denominator(10)
        if abs(float(frac) - x) < 1e-10:
            return f"{frac.numerator}/{frac.denominator}"

        # иначе нормальный float вывод
        return f"{x:.15g}"

    return str(x)

#def format_number(x, tol=1e-10):
#    if isinstance(x, str):
#        return x#
#
#    frac = Fraction(x).limit_denominator(1000)
#    #frac =Fraction(str(x))
#    if abs(float(frac) - x) < tol:
#        if frac.denominator == 1:
#            return f"{frac.numerator}"
#        return f"{frac.numerator}/{frac.denominator}"
#
#    return f"{x:.3g}"

#def format_number(x):
#    if isinstance(x, Fraction):
#        return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)

    return str(x)

def print_butcher_table(method):
    from .utils import load_builtin

    if isinstance(method, str):
        method = load_builtin(method)

    name = method.get("name", "Unknown")
    A = method["A"]
    b = method["b"]
    c = method["c"]

    s = len(b)
    method_type = detect_method_type(method)
    print(f"\nMethod: {name}\n", method_type)

    rows = []
    for i in range(s):
        row = [format_number(c[i], method_type)] + [
            format_number(A[i][j], method_type) for j in range(s)
        ]
        rows.append(row)

    b_row = [""] + [format_number(x, method_type) for x in b]

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