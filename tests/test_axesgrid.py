"""Test AxesGrid (aka ImageGrid)."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import ImageGrid

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    im1 = np.arange(100).reshape((10, 10))
    im2 = im1.T
    im3 = np.flipud(im1)
    im4 = np.fliplr(im2)

    fig = plt.figure(figsize=(4.0, 4.0))
    grid = ImageGrid(
        fig,
        111,  # similar to subplot(111)
        nrows_ncols=(2, 2),  # creates 2x2 grid of Axes
        axes_pad=0.1,  # pad between Axes in inch.
    )

    for ax, im in zip(grid, [im1, im2, im3, im4], strict=False):
        # Iterating over the grid returns the Axes.
        ax.imshow(im)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
