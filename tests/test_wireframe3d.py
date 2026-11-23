"""Regression tests for three-dimensional wireframe export."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import makintikz

mpl.use("Agg")


def test_wireframe3d() -> None:
    x = np.linspace(-2, 2, 5)
    y = np.linspace(-2, 2, 5)
    xx, yy = np.meshgrid(x, y)
    zz = np.sin(xx) * np.cos(yy)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(xx, yy, zz, color="blue")

    code = makintikz.get_tikz_code(
        figure=fig,
        include_disclaimer=False,
    )

    plt.close(fig)

    expected_wireframe_lines = 10
    assert code.count("\\addplot3") == expected_wireframe_lines
    assert "coordinates {" in code
    assert "color=blue" in code


def test_wireframe3d_flat_color_and_width_arrays() -> None:
    x = np.linspace(-1, 1, 3)
    y = np.linspace(-1, 1, 3)
    xx, yy = np.meshgrid(x, y)
    zz = xx**2 + yy**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    collection = ax.plot_wireframe(xx, yy, zz)
    collection.set_color(np.array([0.0, 0.5, 0.0, 1.0]))
    collection.set_linewidth(1.75)

    code = makintikz.get_tikz_code(
        figure=fig,
        include_disclaimer=False,
    )

    plt.close(fig)

    assert "coordinates {" in code
    assert "line width=1.75pt" in code
    assert "color=" in code
