import re

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
import makintikz


@pytest.mark.parametrize("alpha", [None, 0.0, 0.5, 1.0])
def test_legend_opacity(alpha):
    with plt.style.context("classic"):
        fig, ax = plt.subplots()
        try:
            ax.plot([1, 2, 3], [2, 4, 6], label="Test")
            legend = ax.legend(framealpha=alpha)

            code = makintikz.get_tikz_code()

            expected = legend.get_frame().get_alpha()
            if expected is None:
                expected = legend.get_frame().get_facecolor()[3]

            match = re.search(r"fill opacity=([0-9.]+)", code)

            assert match is not None, "Missing numeric legend opacity"
            assert float(match.group(1)) == pytest.approx(expected)
            assert "fill opacity=None" not in code
        finally:
            plt.close(fig)
