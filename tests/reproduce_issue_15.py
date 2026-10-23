import matplotlib.pyplot as plt
import numpy as np
import makintikz

N = np.zeros((512, 512))

plt.rcParams["axes.edgecolor"] = "k"
plt.rcParams["axes.linewidth"] = 3
plt.rcParams["axes.grid"] = False

plt.imshow(N, cmap="gray", clim=(-1, 0))

code = makintikz.get_tikz_code(
    include_disclaimer=False,
)

print(code)

plt.show()