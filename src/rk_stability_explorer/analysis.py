from .stability import stability_function
from .utils import load_builtin  # 


def compute_results(methods, X, Y, Z):
    # 1. загрузить методы (если строки)
    loaded_methods = []

    for m in methods:
        if isinstance(m, str):
            m = load_builtin(m)
        loaded_methods.append(m)

    # 2. считать результаты
    results = []

    for method in loaded_methods:
        R = stability_function(Z, method["A"], method["b"])
        results.append((X, Y, R, method["name"]))

    return results