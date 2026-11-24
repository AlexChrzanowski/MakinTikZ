"""Test 3D quiver plots."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Make the grid
    x, y, z = np.meshgrid(
        np.arange(-0.8, 1, 0.2),
        np.arange(-0.8, 1, 0.2),
        np.arange(-0.8, 1, 0.8),
    )

    # Make the direction data for the arrows
    u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
    v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
    w = np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z)

    ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
