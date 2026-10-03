"""Test plots that have NaN values in them."""

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    data = np.array([1, 2, 3, np.nan])
    err = np.array([1, 2, 3, np.nan])
    plt.bar(range(len(data)), data, yerr=err)
    return plt.gcf()


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
