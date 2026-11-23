"""Regression tests for preserving legend text colors."""

import matplotlib.pyplot as plt

import makintikz


def test_dark_background_legend_text_color() -> None:
    with plt.style.context("dark_background"):
        fig, ax = plt.subplots()
        try:
            ax.plot([0, 1], [0, 1], label="Series")
            ax.legend()

            code = makintikz.get_tikz_code(figure=fig)

            assert "text=white" in code
        finally:
            plt.close(fig)


def test_custom_legend_text_color() -> None:
    fig, ax = plt.subplots()
    try:
        ax.plot([0, 1], [0, 1], label="Series")
        legend = ax.legend()
        for text in legend.get_texts():
            text.set_color("red")

        code = makintikz.get_tikz_code(figure=fig)

        assert "text=red" in code
    finally:
        plt.close(fig)


def test_default_legend_does_not_force_text_color() -> None:
    fig, ax = plt.subplots()
    try:
        ax.plot([0, 1], [0, 1], label="Series")
        ax.legend()

        code = makintikz.get_tikz_code(figure=fig)

        assert "text=white" not in code
    finally:
        plt.close(fig)
