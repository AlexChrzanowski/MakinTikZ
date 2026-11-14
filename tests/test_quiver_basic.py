"""Test basic quiver plot with default scaling."""

# ruff: noqa: FIX002, TD002, TD003
# TODO: The expected test file does not include quiver key handling yet.

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x = np.arange(-10, 10, 1)
    y = np.arange(-10, 10, 1)
    u, v = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    q = ax.quiver(x, y, u, v)
    ax.quiverkey(q, X=0.3, Y=1.1, U=10, label="Quiver key, length = 10", labelpos="E")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
