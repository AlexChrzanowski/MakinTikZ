"""Test that legends are transparent for themes with that feature."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    # Use context manager so seaborn style does not leak into other tests
    with plt.style.context("seaborn-v0_8"):
        x = np.linspace(-3.5, 3.5, 100)

        # Sigmoid and its derivative
        sigmoid = 1 / (1 + np.exp(-x))
        sigmoid_prime = sigmoid * (1 - sigmoid)

        # Tanh and its derivative
        tanh = np.tanh(x)
        tanh_prime = 1 - tanh**2

        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        # Plot Sigmoid
        axs[0].plot(x, sigmoid, label="f")
        axs[0].plot(x, sigmoid_prime, label="f'")
        axs[0].set_title("Sigmoid")
        axs[0].legend(loc="upper left")

        # Plot Tanh
        axs[1].plot(x, tanh, label="f")
        axs[1].plot(x, tanh_prime, label="f'")
        axs[1].set_title("Tanh")
        axs[1].legend(loc="upper left")

        fig.tight_layout()
        return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
