"""Test quiver plots with a legend. Method 2 of plotting legend."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x, y = np.meshgrid(np.linspace(-2, 2, 8), np.linspace(-2, 2, 8))

    fig, ax = plt.subplots()
    ax.quiver(x, y, x, y, color="tab:blue", label="Outward Field")
    ax.quiver(x, y, -y, x, color="tab:orange", label="Rotational Field")

    ax.legend(loc="upper right")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
