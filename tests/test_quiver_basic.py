"""Test basic quiver plot with default scaling."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    X = np.arange(-10, 10, 1)
    Y = np.arange(-10, 10, 1)
    U, V = np.meshgrid(X, Y)

    fig, ax = plt.subplots()
    q = ax.quiver(X, Y, U, V)
    ax.quiverkey(q, X=0.3, Y=1.1, U=10,
                label='Quiver key, length = 10', labelpos='E')

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
