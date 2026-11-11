"""Regression tests for errorbar legend labels (issue #21)."""

import matplotlib.pyplot as plt

import makintikz


def test_errorbar_legend_labels() -> None:
    """Preserve labels for multiple errorbar containers."""
    fig, ax = plt.subplots()

    try:
        ax.errorbar(
            x=[1],
            y=[1],
            yerr=[0.5],
            label="data0",
        )
        ax.errorbar(
            x=[2],
            y=[2],
            yerr=[0.5],
            label="data1",
        )

        ax.legend()

        code = makintikz.get_tikz_code(
            figure=fig,
            include_disclaimer=False,
        )

        assert r"\addlegendentry{data0}" in code
        assert r"\addlegendentry{data1}" in code
        expected_entries = 2
        assert code.count(r"\addlegendentry") == expected_entries
    finally:
        plt.close(fig)
