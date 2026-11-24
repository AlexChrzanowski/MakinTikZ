"""Test 3D quiver plot with colormap and colorbar."""

from typing import TYPE_CHECKING, cast

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    # Create a 3D grid of points
    x, y, z = np.meshgrid(
        np.linspace(-2, 2, 6),
        np.linspace(-2, 2, 6),
        np.linspace(-2, 2, 6),
    )

    # Define a 3D vector field (e.g., rotational vortex with vertical drift)
    u = -y
    v = x
    w = 0.5 * z

    # Compute vector magnitudes to map to colors
    magnitudes = np.sqrt(u**2 + v**2 + w**2)

    # Set up colormap and normalization based on magnitudes
    cmap = plt.get_cmap("viridis")
    norm = mcolors.Normalize(vmin=magnitudes.min(), vmax=magnitudes.max())

    # Flatten magnitudes and map to RGBA colors
    # Note: matplotlib's 3D quiver colors segments in a specific order:
    # first all arrow shafts (N), then two head segments per arrow (2*N).
    flat_mag = magnitudes.ravel()
    arrow_colors = cmap(norm(flat_mag))
    all_colors = np.concatenate([arrow_colors, arrow_colors, arrow_colors], axis=0)

    # Create 3D figure and axis
    fig = plt.figure(figsize=(10, 8))
    ax = cast("Axes3D", fig.add_subplot(111, projection="3d"))

    # Plot the 3D quiver field
    ax.quiver(
        x,
        y,
        z,
        u,
        v,
        w,
        colors=all_colors,
        length=0.45,
        normalize=True,
        arrow_length_ratio=0.3,
        linewidth=1.5,
    )

    # Create a ScalarMappable to attach a colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.1)
    cbar.set_label("Vector Magnitude", fontsize=11)

    # Configure labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Quiver Plot Colored by Vector Magnitude", fontsize=13)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
