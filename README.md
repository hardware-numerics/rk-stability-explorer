# rk-stability-explorer
%Stability analysis and visualization tools for Runge–Kutta methods using Butcher tableaux.
# Runge–Kutta Stability Explorer

Runge–Kutta methods are the brightest gems of numerical analysis —
but picking one blindly is a great way to end up in numerical hell.

So instead of guessing:

> *what does the stability region actually look like?*

This repo is a small playground for answering exactly that.

---

## 🔥 What’s inside

A minimal (and intentionally lightweight) setup to:

* compute **stability regions** for Runge–Kutta methods
* plug in **arbitrary Butcher tableaux**
* compare schemes without committing to a full solver stack

---
## Installation

From GitHub:

pip install git+https://github.com/hardware-numerics/rk-stability-explorer.git

Specific version:

pip install git+https://github.com/hardware-numerics/rk-stability-explorer.git@v0.1.0

## ⚔️ Choose your fighter

A curated mix of methods — from well-behaved classics to more… opinionated schemes:

**The usual suspects**

* Euler
* Heun
* RK4

**Accuracy with supervision**

* Dormand–Prince (embedded pair)

**Heavy artillery (stiff problems)**

* Gauss–Legendre
* Radau

**Specialized operators**

* SSP (for when monotonicity matters)
* Williamson low-storage (when memory is tight)
* SDIRK (for those who like compromises)
* PseudoSymplectic (a real diamond :))

Some of these behave beautifully.
Some don’t. That’s the point.

---

## 📈 Stability regions

*(insert your figure here)*

Top row: stability regions growing left → right.
Translation: larger timesteps, fewer regrets.

---

## 🧪 What you can actually do here

* Visualize stability regions
* Compare methods side by side
* Stress-test schemes against your intuition
* Drop in your own RK method and see if it survives

---

## 🧾 Bring your own method

All methods are defined via **Butcher tableaux** in YAML.

It’s simple, explicit, and slightly annoying —
which is exactly what you want when things start breaking.

---

## 🚀 Quick start

```bash id="91dks2"
git clone https://github.com/hardware-numerics/rk-stability-explorer
cd rk-stability-explorer
```

Then open:

* `notebooks/stability_demo.ipynb` — interactive walkthrough
* `rk/` — core logic
* `methods/` — method definitions

---

## 🎓 Why this exists

Originally put together for a course on advanced numerical methods.

Because stability regions are too important to stay abstract —
and too fun not to plot.

---

## 💬 Final note

If your favorite RK method is missing — add it.

Or defend it.

Both are equally welcome.

