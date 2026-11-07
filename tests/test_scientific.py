"""Tests that data returns the correct scientific notation.

Given that strict=True, should strictly match the style of Matplotlib.
By default, scilimits is [-5,6]
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot_lower_limit() -> Figure:
    fig, ax = plt.subplots()
    order_of_magnitude = -5
    data = np.arange(4) * (10**order_of_magnitude)
    ax.plot(data, [1, 4, 2, 3])
    return fig


def plot_upper_limit() -> Figure:
    fig, ax = plt.subplots()
    order_of_magnitude = 6
    data = np.arange(4) * (10**order_of_magnitude)
    ax.plot(data, [1, 4, 2, 3])
    return fig


def plot_fixed() -> Figure:
    fig, ax = plt.subplots()
    order_of_magnitude = 0
    data = np.arange(4) * (10**order_of_magnitude)
    ax.plot(data, [1, 4, 2, 3])
    return fig


def test() -> None:
    assert_equality(plot_lower_limit, __file__[:-3] + "_lower_reference.tex", strict=True)
    assert_equality(plot_upper_limit, __file__[:-3] + "_upper_reference.tex", strict=True)
    assert_equality(plot_fixed, __file__[:-3] + "_fixed_reference.tex", strict=True)
