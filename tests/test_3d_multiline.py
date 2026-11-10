"""Test multiple 3D line plots."""

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
    fig = plt.figure(figsize=(8, 6))
    ax = cast("Axes3D", fig.add_subplot(projection="3d"))

    # Line 1: Spiral curve
    t = np.linspace(0, 10, 100)
    x1 = np.sin(t)
    y1 = np.cos(t)
    z1 = t
    ax.plot(x1, y1, z1, label="Spiral Line", color="blue", linewidth=2)

    # Line 2: Shifted helix curve
    x2 = np.sin(t) + 1
    y2 = np.cos(t) + 1
    z2 = t
    ax.plot(x2, y2, z2, label="Shifted Helix", color="red", linestyle="--", linewidth=2)

    # Line 3: Straight diagonal line
    x3 = np.linspace(-1, 2, 50)
    y3 = np.linspace(-1, 2, 50)
    z3 = np.linspace(0, 10, 50)
    ax.plot(x3, y3, z3, label="Diagonal Line", color="green", marker="o", markersize=3)

    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title("Multiple 3D Lines Example")
    ax.legend()

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
