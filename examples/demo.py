import numpy as np
import matplotlib.pyplot as plt
import rk_stability_explorer as rk

#print(rk_stability_explorer.__file__)


#methods = [
#    "euler", "rk4", "dopri5",
#    "optRK62", "ps36", "williamson",
#    "ssprk33", "kvarno", "radauIIA"
#]

methods = [
    "euler", "heun", "rk4", "dopri5",
    "optRK62", "radauIIA", "kvarno", "williamson",
    "ssprk33","ps36"
]



X, Y = rk.make_grid(n=200)
Z = X + 1j * Y

results = rk.compute_results(methods, X, Y, Z)
fig = rk.rkplot_multiple(results, cols=5, cmap = "twilight")

fig.savefig("DemoRK.png",  dpi=200, bbox_inches = 'tight', pad_inches = 0)
plt.show()
