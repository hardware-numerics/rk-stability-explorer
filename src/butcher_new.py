#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 00:17:07 2026

@author: hardware-numerics
"""

import yaml
import numpy as np
from fractions import Fraction

# ---------- parser ----------
def _parse(x, context):
    if isinstance(x, (int, float)):
        return float(x)

    if isinstance(x, str):
        x = x.strip()

        safe_dict = {
            "sqrt": np.sqrt,
            "pi": np.pi,
        }
        safe_dict.update(context)

        # fraction fast-path
        if "/" in x and all(c in "0123456789./- " for c in x):
            try:
                return float(Fraction(x))
            except:
                pass

        return float(eval(x, {"__builtins__": {}}, safe_dict))

    raise TypeError(f"Unsupported type: {type(x)}")


def _parse_matrix(M, ctx):
    return np.array([[_parse(x, ctx) for x in row] for row in M])


def _parse_vector(v, ctx):
    return np.array([_parse(x, ctx) for x in v])


# ---------- loader ----------
def load_method(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    params = data.get("params", {})

    method = {
        "name": data.get("name", "RK method"),
        "type": data.get("type", "rk"),
    }

    # ---- standard RK ----
    if "A" in data:
        A = _parse_matrix(data["A"], params)
        b = _parse_vector(data["b"], params)

        method["A"] = A
        method["b"] = b

        # c handling
        if data.get("c", None) == "auto":
            method["c"] = A.sum(axis=1)
        else:
            method["c"] = _parse_vector(data["c"], params)

    # ---- embedded ----
    if "b_alt" in data:
        method["b_alt"] = _parse_vector(data["b_alt"], params)

    # ---- IMEX ----
    if data.get("type") == "imex":
        method["A_explicit"] = _parse_matrix(data["A_explicit"], params)
        method["A_implicit"] = _parse_matrix(data["A_implicit"], params)
        method["b_explicit"] = _parse_vector(data["b_explicit"], params)
        method["b_implicit"] = _parse_vector(data["b_implicit"], params)

        if data.get("c", None) == "auto":
            method["c"] = method["A_explicit"].sum(axis=1)

    # ---- checks ----
    if "A" in method:
        s = method["A"].shape[0]
        assert method["A"].shape == (s, s)
        assert len(method["b"]) == s

    return method

