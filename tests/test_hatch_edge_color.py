"""Regression tests for Matplotlib hatch edge-color handling."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import makintikz

mpl.use("Agg")


@pytest.mark.parametrize(
    ("edgecolor", "expected_color"),
    [
        ("red", "red"),
        ("blue", "blue"),
        ("none", "black"),
    ],
)
def test_hatch_inherits_edge_color(edgecolor: str, expected_color: str) -> None:
    """Verify that hatch patterns inherit the correct edge color."""
    fig, ax = plt.subplots()

    try:
        bars = ax.bar(
            [0],
            [1],
            width=0.5,
            facecolor="white",
            edgecolor=edgecolor,
            hatch="/",
        )

        patch = bars.patches[0]
        assert patch.get_hatch() == "/"

        code = makintikz.get_tikz_code(figure=fig)

        assert "pattern=" in code

        if expected_color == "black":
            # TikZ uses black when no pattern color is specified.
            assert "pattern color=" not in code
        else:
            assert f"pattern color={expected_color}" in code
    finally:
        plt.close(fig)
