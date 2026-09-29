"""Test colorfill with log scale and zero minimum."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    rc_params = {"figure.figsize": [5, 5], "figure.dpi": 220, "pgf.rcfonts": False}

    with plt.rc_context(rc=rc_params):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.fill_between(np.arange(3), 0, 1)
        ax.fill_between(np.arange(3), 1, 10)

        ax.set_title("Colorfill log and 0")
        ax.set_yscale("log")

        return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
