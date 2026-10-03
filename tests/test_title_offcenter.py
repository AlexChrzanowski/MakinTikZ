"""Test that the title is correctly placed offcenter (right side) of the figure."""

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    z = np.random.default_rng().integers(0, 2, size=(10, 10))

    fig, ax = plt.subplots(figsize=(9, 9))

    ax.imshow(z, origin="lower", cmap="coolwarm")

    ax.set_title("My Title\n" + "Subtext", loc="right")

    plt.tight_layout()

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
