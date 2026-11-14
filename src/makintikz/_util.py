"""Several utility functions used at various parts of makintikz library."""

from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

import matplotlib.transforms
import numpy as np

if TYPE_CHECKING:
    from matplotlib.artist import Artist
    from matplotlib.axes import Axes
    from matplotlib.legend import Legend
    from matplotlib.lines import Line2D
    from mpl_toolkits.mplot3d import Axes3D


def has_legend(axes: Axes | Axes3D) -> bool:
    return axes.get_legend() is not None


def _find_legend(axes: Axes) -> Legend | None:
    """Return the legend attached to axes, or the first legend found on the figure."""
    leg = axes.get_legend()
    if leg is not None:
        return leg

    for ax in axes.figure.axes:
        other_leg = ax.get_legend()
        if other_leg is not None:
            return other_leg

    return None


def _get_legend_handles(leg: Legend) -> list[Artist | None]:
    """Return legend handles across Matplotlib versions."""
    try:
        return leg.legend_handles  # matplotlib version >= 3.7.0
    except AttributeError:
        return leg.legendHandles  # type: ignore[attr-defined]  # matplotlib version < 3.7.0


def _match_direct_or_labeled_handle(
    obj: Artist,
    leg: Legend,
    leg_handles: list[Artist | None],
) -> str | None:
    """Match an artist against legend handles by identity, explicit label, or axes handles."""
    for handle, text in zip(leg_handles, leg.texts, strict=True):
        if handle is obj:
            return text.get_text()

    label = obj.get_label()
    if isinstance(label, str) and label and not label.startswith("_"):
        label_map = {
            h.get_label(): t.get_text()
            for h, t in zip(leg_handles, leg.texts, strict=True)
            if h is not None
        }
        if label in label_map:
            return label_map[label]

    # Check actual axes handles/labels (matches Quiver/Collection artists directly)
    ax_handles, ax_labels = obj.axes.get_legend_handles_labels()
    for handle, ax_label in zip(ax_handles, ax_labels, strict=True):
        if handle is obj:
            return ax_label

    return None


def _match_positional_legend_text(
    obj: Artist,
    leg: Legend,
    leg_handles: list[Artist | None],
) -> str | None:
    """Positional fallback when labels are passed directly to ax.legend(["A", "B"])."""
    label = obj.get_label()
    if not (isinstance(label, str) and label.startswith("_") and label != "_nolegend_"):
        return None

    all_artists = [
        a for a in (*obj.axes.lines, *obj.axes.patches, *obj.axes.collections) if a is not leg
    ]
    claimed_labels = {
        a.get_label()
        for a in all_artists
        if isinstance(a.get_label(), str) and a.get_label() and not a.get_label().startswith("_")
    }
    claimed_handles = set(all_artists)

    unclaimed_texts = [
        text.get_text()
        for handle, text in zip(leg_handles, leg.texts, strict=True)
        if handle not in claimed_handles
        and (handle is None or handle.get_label() not in claimed_labels)
    ]
    if not unclaimed_texts:
        return None

    candidates = [
        a
        for a in all_artists
        if a not in leg_handles
        and isinstance(a.get_label(), str)
        and a.get_label().startswith("_")
        and a.get_label() != "_nolegend_"
    ]
    if obj in candidates:
        idx = candidates.index(obj)
        if idx < len(unclaimed_texts):
            return unclaimed_texts[idx]

    return None


def get_legend_text(obj: Artist) -> str | None:
    """Check if object is in legend."""
    if obj.axes is None:
        return None

    leg = _find_legend(obj.axes)
    if leg is None:
        return None

    leg_handles = _get_legend_handles(leg)

    direct_match = _match_direct_or_labeled_handle(obj, leg, leg_handles)
    if direct_match is not None:
        return direct_match

    return _match_positional_legend_text(obj, leg, leg_handles)


def transform_to_data_coordinates(
    obj: Line2D, xdata: np.ndarray, ydata: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The coordinates might not be in data coordinates, but could be sometimes in axes coordinates.

    For example, the matplotlib command
      axes.axvline(2)
    will have the y coordinates set to 0 and 1, not to the limits. Therefore, a
    two-stage transform has to be applied:
      1. first transforming to display coordinates, then
      2. from display to data.
    """
    if obj.axes is not None and obj.get_transform() != obj.axes.transData:
        points = np.array([xdata, ydata]).T
        transform = matplotlib.transforms.composite_transform_factory(
            obj.get_transform(), obj.axes.transData.inverted()
        )
        xdata, ydata = transform.transform(points).T
        return xdata, ydata
    return xdata, ydata


_NO_ESCAPE = r"(?<!\\)(?:\\\\)*"
_split_math = re.compile(_NO_ESCAPE + r"\$").split
_replace_mathdefault = functools.partial(
    # Replace \mathdefault (when not preceded by an escape) by empty string.
    re.compile(_NO_ESCAPE + r"(\\mathdefault)").sub,
    "",
)


def _common_texification(text: str) -> str:
    return _tex_escape(text)


# https://github.com/nschloe/tikzplotlib/pull/603
def _tex_escape(text: str) -> str:
    r"""Do some necessary and/or useful substitutions for texts to be included in LaTeX documents.

    This distinguishes text-mode and math-mode by replacing the math separator
    ``$`` with ``\(\displaystyle %s\)``. Escaped math separators (``\$``)
    are ignored.
    """
    # Sometimes, matplotlib adds the unknown command \mathdefault.
    # Not using \mathnormal instead since this looks odd for the latex cm font.
    text = _replace_mathdefault(text)
    text = text.replace("\N{MINUS SIGN}", r"\ensuremath{-}")
    # Work around <https://github.com/matplotlib/matplotlib/issues/15493>
    text = text.replace("&", r"\&")
    text = text.replace("_", r"\_")
    text = text.replace("%", r"\%")
    # split text into normaltext and inline math parts
    parts = _split_math(text)
    for i, s in enumerate(parts):
        if i % 2:  # mathmode replacements
            parts[i] = rf"\(\displaystyle {s}\)"
    return "".join(parts)
