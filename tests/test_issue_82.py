"""Regression tests for issue #82: linewidth translation."""

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import pytest

import makintikz


@pytest.mark.parametrize(
    ("width", "strict", "expected"),
    [
        (2.5, False, "line width=1pt"),
        (2.5, True, "line width=2.5pt"),
        (4.0, True, "line width=4pt"),
        (0.5, True, "line width=0.5pt"),
    ],
)
def test_linewidth_translation(width: float, *, strict: bool, expected: str) -> None:
    fig, ax = plt.subplots()
    try:
        ax.plot([0, 1, 2], [1, 3, 2], linewidth=width)
        code = makintikz.get_tikz_code(figure=fig, strict=strict)

        plot_lines = [line for line in code.splitlines() if line.startswith("\\addplot [")]

        assert len(plot_lines) == 1
        assert expected in plot_lines[0]
    finally:
        plt.close(fig)
