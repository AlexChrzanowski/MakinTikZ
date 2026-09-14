"""Test tick positioning."""

import itertools
import makintikz
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]

    fig = plt.figure(figsize=(10, 10))

    # repeat=4 gives 16 combinations of (bottom, top, left, right)
    for i, (bottom, top, left, right) in enumerate(itertools.product([False, True], repeat=4)):
        ax = plt.subplot(4, 4, i + 1)
        plt.plot(x, y, "ro")

        # Set the visibility of the tick lines
        # We also turn off the labels so the plots don't overlap
        ax.tick_params(axis="x", which="both", bottom=bottom, top=top, labelbottom=False)
        ax.tick_params(axis="y", which="both", left=left, right=right, labelleft=False)

    plt.tight_layout()
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")


def test_hidden_ticks_keep_labels() -> None:
    fig, ax = plt.subplots()

    ax.plot([0, 1], [0, 1])

    # Hide x-axis tick marks, but keep labels visible
    ax.tick_params(
        axis="x",
        which="both",
        bottom=False,
        top=False,
        labelbottom=True,
    )

    code = makintikz.get_tikz_code(
        include_disclaimer=False,
        float_format=".8g",
    )

    plt.close("all")

    assert "xtick style={draw=none}" in code
    assert "xmajorticks=false" not in code

def test_hidden_ticks_and_labels_disable_ticks() -> None:
    fig, ax = plt.subplots()

    ax.plot([0, 1], [0, 1])

    # Hide both x-axis tick marks and labels
    ax.tick_params(
        axis="x",
        which="both",
        bottom=False,
        top=False,
        labelbottom=False,
    )

    code = makintikz.get_tikz_code(
        include_disclaimer=False,
        float_format=".8g",
    )

    plt.close("all")

    assert "xmajorticks=false" in code
