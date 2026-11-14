"""Test basic quiver plot with 'inch' scaling."""

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
    fig, ax2 = plt.subplots()
    ax2.set_title("pivot='middle'; every third arrow; units='inches'")
    Q = ax2.quiver(X[::3, ::3], Y[::3, ::3], U[::3, ::3], V[::3, ::3],
                pivot='middle', units='inches')
    qk = ax2.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                    coordinates='figure')
    ax2.scatter(X[::3, ::3], Y[::3, ::3], color='r', s=5)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
