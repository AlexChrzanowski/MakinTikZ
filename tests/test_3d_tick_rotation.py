"""Test 3D plot with rotated z-axis tick labels."""

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

    # 3D line plot (helix)
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 60)
    z = np.linspace(-2, 2, 60)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, z)

    # Apply specific rotation to z-axis tick labels
    ax.tick_params(axis="z", rotation=45)
    # Apply a distinct rotation to x-axis tick labels to ensure independence
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=90)

    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
