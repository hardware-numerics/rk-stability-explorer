# rk-stability-explorer
Stability analysis and visualization tools for Runge–Kutta methods using Butcher's tableux

![RK stability plot](examples/DemoRK.png) 

Top row: stability regions growing left → right.Translation: larger timesteps, fewer regrets.

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

<pre> pip install --upgrade --no-cache-dir  git+https://github.com/hardware-numerics/rk-stability-explorer.git</pre>

Specific version:

<pre> pip install --upgrade --no-cache-dir  git+https://github.com/hardware-numerics/rk-stability-explorer.git@v0.1.0 </pre>

## Installation in virtual enironment 

to use package inside virtualenv (assuming virtualenv tool is installed into system-wide python):

```
$ mkdir ~/apps
$ mkdir ~/apps/myutil
$ cd ~/apps/myutil
$ virtualenv .env
$ source .env/bin/activate
(.env)$ pip install --upgrade --no-cache-dir  git+https://github.com/hardware-numerics/rk-stability-explorer.git
```

## Quick usage examples

run from terminal to list implemented methods

```
rk-stability list

explicit | williamson, euler, optRK4, spijker, ssprk33, optRK62, explicit_midpoint, ps36, heun, rk4, skewedrk4, dopri5, dop853, rk3, bogacki_shampine
implicit | gauss_legendre_2, implicit_midpoint, kvarno, ars22, radauIIA, BDF2
```
print Butcher's tableux

```
rk-stability show rk4

Method: Classical RK4

  0 │   0    0    0    0
1/2 │ 1/2    0    0    0
1/2 │   0  1/2    0    0
  1 │   0    0    1    0
──────────────────────────────
    │ 1/6  1/3  1/3  1/6


```


## Plotting from CLI


```
rk-stability plot rk4 heun 
```

```
rk-stability plot rk4 heun radauIIA --cols 3 --save rktest.png
```
![cli print RK](examples/rktest.png)


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

## Tutorials&Demos

* `notebooks/rk-basic-tutorial.ipynb` — interactive walkthrough
* `notebooks/demo.py` — demo
* `rk_stability_explorer/` — core logic
* `rk_stability_explorer/methods/` — methods are here

---

## 🎓 Why this exists

Originally put together for a course on advanced numerical methods.

Because stability regions are too important to stay abstract —
and too fun not to plot.

---

## 💬 Final note

If your favorite RK method is missing — add it. The package is experimental and intentinally 
light-weighted and meant to encourage  students from Advanced Numerical Methods for Physics and Medical Physics" (SoSe2026, HHU) 
are especially welcome to contribute :)


