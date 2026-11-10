"""Regression tests for preserving axis edge width (issue #15)."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest

import makintikz


@pytest.mark.parametrize("linewidth", [0.5, 1.0, 2.0, 3.0])
def test_axis_edge_width(linewidth: float) -> None:
    """Preserve Matplotlib axis border widths in PGFPlots."""
    with mpl.rc_context(
        {
            "axes.edgecolor": "k",
            "axes.linewidth": linewidth,
            "axes.grid": False,
        }
    ):
        fig, ax = plt.subplots()

        try:
            ax.imshow(
                np.zeros((8, 8)),
                cmap="gray",
                vmin=-1,
                vmax=0,
            )

            code = makintikz.get_tikz_code(
                figure=fig,
                include_disclaimer=False,
            )

            assert f"line width={linewidth:g}pt" in code
        finally:
            plt.close(fig)
