"""Test plots with nan values that should produce gaps in the line."""

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    ypoints = np.array([3, 8, np.nan, 1, 10])
    plt.plot(ypoints)
    return plt.gcf()


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
