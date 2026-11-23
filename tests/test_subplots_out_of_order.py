"""Test subplots accessed out of grid order. Test case for Issue #42."""

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()

    plt.subplot(3, 1, 3)
    plt.plot([0, 0, 0])

    plt.subplot(3, 1, 2)
    plt.plot([3, 4, 5])

    plt.subplot(3, 1, 1)
    plt.plot([1, 2, 2])

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
