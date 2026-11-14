"""Test quiver plot with a colormap, colorbar, and 'x' scaling."""

# TODO: The expected test file does not include quiver key handling yet.

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x, y = np.meshgrid(np.arange(0, 2 * np.pi, 0.2), np.arange(0, 2 * np.pi, 0.2))
    u = np.cos(x)
    v = np.sin(y)

    fig, ax3 = plt.subplots()
    ax3.set_title("pivot='tip'; scales with x view")
    m = np.hypot(u, v)
    q = ax3.quiver(x, y, u, v, m, units="x", pivot="tip", width=0.022, scale=1 / 0.15)
    ax3.quiverkey(q, 0.9, 0.9, 1, r"$1 \frac{m}{s}$", labelpos="E", coordinates="figure")
    ax3.scatter(x, y, color="0.5", s=1)
    fig.colorbar(q, ax=ax3, label="Magnitude")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
