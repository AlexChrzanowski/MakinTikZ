"""Test markevery option with a legend."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, ax = plt.subplots(figsize=(2, 1.5), dpi=300)
    psi_0 = np.linspace(0, 2 * np.pi, 360)

    ax.plot(
        np.rad2deg(psi_0),
        np.sin(psi_0),
        "-",
        label="n=1",
        marker=Line2D.filled_markers[1],
        markevery=[25, 99, 165, 275],
    )

    ax.legend(bbox_to_anchor=(0, 1.20), loc="upper left", ncol=3)
    ax.set_xlim(0, 360)
    ax.set_xticks(np.arange(0, 361, step=180))

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
