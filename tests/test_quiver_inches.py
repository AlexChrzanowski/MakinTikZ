"""Test basic quiver plot with 'inch' scaling."""

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
    fig, ax2 = plt.subplots()
    ax2.set_title("pivot='middle'; every third arrow; units='inches'")
    q = ax2.quiver(
        x[::3, ::3], y[::3, ::3], u[::3, ::3], v[::3, ::3], pivot="middle", units="inches"
    )
    ax2.quiverkey(q, 0.9, 0.9, 1, r"$1 \frac{m}{s}$", labelpos="E", coordinates="figure")
    ax2.scatter(x[::3, ::3], y[::3, ::3], color="r", s=5)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
