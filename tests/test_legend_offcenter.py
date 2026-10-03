"""Test that the legend is correctly placed offcenter (left side) of the figure."""

import matplotlib as mpl
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    z = np.random.default_rng().integers(0, 2, size=(10, 10))

    fig, ax = plt.subplots(figsize=(9, 9))

    im = ax.imshow(z, origin="lower", cmap="coolwarm")

    colors = [im.cmap(im.norm(v)) for v in [0, 1]]  # type: ignore[misc]

    patches = [
        mpatches.Patch(color=colors[i], label=text) for i, text in enumerate(["Label 1", "Label 2"])
    ]

    ax.legend(
        handles=patches, bbox_to_anchor=(0, 1), loc="lower left", borderaxespad=0.1, frameon=False
    )

    plt.tight_layout()

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
