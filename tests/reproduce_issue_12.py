import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import makintikz

fig, ax = plt.subplots()

ax.set_ylim([0.635, 0.665])
ax.grid()

# Force exactly 3 decimal places
ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))

code = makintikz.get_tikz_code(
    include_disclaimer=False,
)

print(code)

plt.show()