"""Test log-scale histogram with synthetic bounding box distribution."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    rng = np.random.Generator(np.random.PCG64(42))

    data = rng.lognormal(mean=2.7, sigma=0.75, size=40000)

    median_val = int(np.round(np.median(data)))
    mean_val = int(np.round(np.mean(data)))

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

    bins = np.arange(0, np.max(data) + 2, 2).tolist()
    ax.hist(data, bins=bins, log=True)

    ax.set_xlim(left=0)
    ax.set_title(
        f"Bounding Box height pixel overview\nmedian = {median_val} px, mean = {mean_val} px",
        fontsize=14,
    )
    ax.set_xlabel("object instance bounding box height", fontsize=13)
    ax.set_ylabel("number of objects", fontsize=13)

    ax.tick_params(axis="both", which="both", direction="out", labelsize=12)

    fig.tight_layout()
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
