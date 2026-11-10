"""Test 3D plot tick direction alignment in strict mode."""

from typing import TYPE_CHECKING, cast

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    ax = cast("Axes3D", fig.add_subplot(projection="3d"))

    t = np.linspace(0, 10, 50)
    ax.plot(np.cos(t), np.sin(t), t)

    # In Matplotlib 3D, axis="both" only covers x and y; z must be specified explicitly
    for axis_name in ("x", "y", "z"):
        ax.tick_params(axis=axis_name, which="both", direction="out")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    return fig


def test() -> None:
    # Set strict=True to activate 3D tick direction export
    assert_equality(plot, __file__[:-3] + "_reference.tex", strict=True)
