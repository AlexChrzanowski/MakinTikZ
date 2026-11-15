import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import makintikz


def test_wireframe3d():
    x = np.linspace(-2, 2, 5)
    y = np.linspace(-2, 2, 5)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(X, Y, Z, color="blue")

    code = makintikz.get_tikz_code(
        figure=fig,
        include_disclaimer=False,
    )

    plt.close(fig)

    assert code.count("\\addplot3") == 10
    assert "coordinates {" in code
    assert "color=blue" in code
