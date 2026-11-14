"""Test quiver plot with a colormap, colorbar, and 'x' scaling."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
    U = np.cos(X)
    V = np.sin(Y)

    fig, ax3 = plt.subplots()
    ax3.set_title("pivot='tip'; scales with x view")
    M = np.hypot(U, V)
    Q = ax3.quiver(X, Y, U, V, M, units='x', pivot='tip', width=0.022,
                scale=1 / 0.15)
    qk = ax3.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                    coordinates='figure')
    ax3.scatter(X, Y, color='0.5', s=1)
    fig.colorbar(Q, ax=ax3, label="Magnitude")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
