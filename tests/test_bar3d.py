"""Regression tests for basic three-dimensional bar export."""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import makintikz


def test_bar3d_rectangular_patches() -> None:
    """Export two bars, each made of six four-corner rectangular faces."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    try:
        bars = ax.bar3d(
            [0, 1],
            [0, 1],
            [0, 0],
            [0.5, 0.5],
            [0.5, 0.5],
            [2, 3],
            color="blue",
            shade=False,
        )
        assert isinstance(bars, Poly3DCollection)
        code = makintikz.get_tikz_code(figure=fig, include_disclaimer=False)
        expected_faces = 12
        corners_per_face = 4
        assert code.count(r"\addplot3") == 1
        assert "patch type=rectangle" in code
        assert "fill=blue" in code
        assert code.count("coordinates {") == 1
        # Count coordinate tuples in the patch block, not all surrounding TeX.
        patch_data = code.split("patch type=rectangle", maxsplit=1)[1].split("};", maxsplit=1)[0]
        assert patch_data.count("(") == expected_faces * corners_per_face
        assert "(1.5, 1.5, 3)" in patch_data
    finally:
        plt.close(fig)
