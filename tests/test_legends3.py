"""Test legends to ensure symbols are correct. Test case for Issue #30."""

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()

    plt.imshow([[1, 2], [3, 4]])

    plt.plot(0, 0, "x", label="0")
    plt.plot(0, 1, "x", label="1")
    plt.plot(1, 0, "x", label="2")
    plt.plot(1, 1, "x", label="3")

    plt.legend()

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
