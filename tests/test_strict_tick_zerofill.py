"""Regression tests for preserving tick-label precision in strict mode."""

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import makintikz


def test_strict_preserves_independent_axis_precision() -> None:
    fig, ax = plt.subplots()
    try:
        ax.plot([0.001, 0.002], [1, 2])
        ax.set_xticks([0.001, 0.0015, 0.002])
        ax.set_yticks([1, 1.5, 2])

        ax.xaxis.set_major_formatter(FormatStrFormatter("%.4f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

        fig.canvas.draw()
        code = makintikz.get_tikz_code(figure=fig, strict=True)

        assert "xticklabels={0.0010,0.0015,0.0020}" in code
        assert "yticklabels={1.0,1.5,2.0}" in code
    finally:
        plt.close(fig)


def test_strict_preserves_two_decimal_places() -> None:
    fig, ax = plt.subplots()
    try:
        ax.plot([0, 2], [0, 2])
        ax.set_xticks([0, 1, 2])
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        fig.canvas.draw()
        code = makintikz.get_tikz_code(figure=fig, strict=True)

        assert "xticklabels={0.00,1.00,2.00}" in code
    finally:
        plt.close(fig)
