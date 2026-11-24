"""Test AxisGrid/ImageGrid."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cbook
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import ImageGrid

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure(figsize=(5.5, 3.5))
    grid = ImageGrid(
        fig,
        111,  # similar to subplot(111)
        nrows_ncols=(1, 3),
        axes_pad=0.1,
        label_mode="L",
    )

    # demo image
    z = np.load(cbook.get_sample_data("axes_grid/bivariate_normal.npy", asfileobj=False))
    im1 = z
    im2 = z[:, :10]
    im3 = z[:, 10:]
    vmin, vmax = z.min(), z.max()
    for ax, im in zip(grid, [im1, im2, im3], strict=False):
        ax.imshow(im, origin="lower", vmin=vmin, vmax=vmax)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex", strict=True)
