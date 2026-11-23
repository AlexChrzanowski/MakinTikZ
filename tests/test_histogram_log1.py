"""Test histogram with logarithmic scale."""

import matplotlib as mpl
import pandas as pd
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    plot_values = pd.DataFrame(
        {
            "test0": pd.Series([0, 0, 0, 0.1, 0.1, 0.2]),
            "test1": pd.Series([0, 0.1]),
        }
    )
    ax = plot_values.plot.hist(stacked=False)
    fig = ax.get_figure()

    fig.set_size_inches(4, 3)
    ax.set_yscale("log")
    ax.set_ylim(bottom=0.1)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
