from .stability import stability_function
from .utils import load_builtin  # 
import numpy as np

def compile_method(method):
    A = np.array(method["A"], dtype=float)
    b = np.array(method["b"], dtype=float)

    c = method.get("c", None)

    if c is None:
        # fallback: row sums
        c = np.sum(A, axis=1)
    else:
        c = np.array(c, dtype=float)

    return {
        "A": A,
        "b": b,
        "c": c,
        "name": method["name"]
    }
    
   

def compute_results(methods, X, Y, Z):
    # 1. load methods (strings)
    loaded_methods = []

    for m in methods:
        if isinstance(m, str):
            m = load_builtin(m)
        m = compile_method(m)   # make it float
        loaded_methods.append(m)

    # 2. compute results
    results = []

    for method in loaded_methods:
        R = stability_function(Z, method["A"], method["b"])
        results.append((X, Y, R, method["name"]))

    return results