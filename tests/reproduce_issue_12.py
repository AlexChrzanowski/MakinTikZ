"""Regression tests for formatted tick-label precision (issue #12)."""

import matplotlib.pyplot as plt
import pytest
from matplotlib.ticker import FormatStrFormatter

import makintikz


@pytest.mark.parametrize(
    ("format_string", "expected_label"),
    [
        ("%.3f", "0.640"),
        ("%.2f", "0.64"),
        ("%.4f", "0.6400"),
    ],
)
def test_formatted_tick_precision(format_string: str, expected_label: str) -> None:
    """Preserve the formatter's requested decimal precision."""
    fig, ax = plt.subplots()

    try:
        ax.set_ylim(0.635, 0.665)
        ax.set_yticks([0.640])
        ax.yaxis.set_major_formatter(FormatStrFormatter(format_string))

        code = makintikz.get_tikz_code(
            figure=fig,
            include_disclaimer=False,
        )

        assert expected_label in code
    finally:
        plt.close(fig)
