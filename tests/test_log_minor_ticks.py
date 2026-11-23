"""Test log-log scatter plot with custom minor y-ticks."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x = [
        0.00404784042977909,
        0.140660747273482,
        0.294901125967985,
        0.603381883356992,
        0.779656601864995,
        0.9779656601865,
    ]
    y = [0.763156, 0.92578, 0.979844, 0.9997, 1.0, 1.0]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(x, y)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid()

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
