"""Test 3D scatter plot with multiple markers and ranges."""

from typing import TYPE_CHECKING, cast

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

from .helpers import assert_equality

mpl.use("Agg")


def randrange(rng: np.random.Generator, n: int, vmin: float, vmax: float) -> np.ndarray:
    """Helper function to make an array of random numbers uniformly distributed."""
    return rng.uniform(vmin, vmax, n)


def plot() -> Figure:
    rng = np.random.default_rng(19680801)

    fig = plt.figure()
    ax = cast("Axes3D", fig.add_subplot(projection="3d"))

    n = 100

    for m, zlow, zhigh in [("o", -50, -25), ("^", -30, -5)]:
        xs = randrange(rng, n, 23, 32)
        ys = randrange(rng, n, 0, 100)
        zs = randrange(rng, n, zlow, zhigh)
        ax.scatter(xs, ys, zs, marker=m)

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
