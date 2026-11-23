"""Regression tests for text bounding-box arrow styles."""

import matplotlib.pyplot as plt
import pytest

import makintikz


@pytest.mark.parametrize(
    ("boxstyle", "expected", "unexpected"),
    [
        ("rarrow", "single arrow", "shape border rotate=180"),
        ("larrow", "shape border rotate=180", "double arrow"),
        ("darrow", "double arrow", "single arrow"),
    ],
)
def test_bbox_arrow_style(
    boxstyle: str,
    expected: str,
    unexpected: str,
) -> None:
    """Verify that arrow box styles generate the correct TikZ options."""
    fig, ax = plt.subplots()
    try:
        ax.text(
            0.5,
            0.5,
            "Arrow",
            bbox={"boxstyle": boxstyle},
        )

        code = makintikz.get_tikz_code()

        assert expected in code
        assert unexpected not in code
    finally:
        plt.close(fig)
