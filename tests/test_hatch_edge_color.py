import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
import makintikz


@pytest.mark.parametrize(
    ("edgecolor", "expected_color"),
    [
        ("red", "red"),
        ("blue", "blue"),
        ("none", "black"),
    ],
)
def test_hatch_inherits_edge_color(edgecolor, expected_color):
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

        code = makintikz.get_tikz_code()

        print(f"\nEdge color: {edgecolor}")
        print(f"Hatch color: {patch._hatch_color!r}")
        print(code)

        assert "pattern" in code
        assert "pattern color" in code or expected_color == "black"
    finally:
        plt.close(fig)
