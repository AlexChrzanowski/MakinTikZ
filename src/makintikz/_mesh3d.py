"""Convert Matplotlib 3D wireframe meshes to PGFPlots."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from . import _color

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    from ._tikzdata import TikzData

ARRAY_DIMENSIONS = 2
RGB_CHANNELS = 3
RGBA_CHANNELS = 4
MIN_SEGMENT_POINTS = 2


def _normalize_color_cycle(values: np.ndarray | list | tuple) -> list:
    """Normalize Matplotlib color values to one list entry per segment."""
    if values is None:
        return []

    array = np.asarray(values)
    if array.size == 0:
        return []
    if array.ndim == 0:
        return [array.item()]
    if array.ndim == 1 and array.shape[0] in (3, 4):
        return [array]
    if array.ndim == ARRAY_DIMENSIONS and array.shape[1] in (RGB_CHANNELS, RGBA_CHANNELS):
        return list(array)
    return array.tolist()


def _normalize_scalar_cycle(values: np.ndarray | list | tuple) -> list:
    """Normalize non-color scalar values such as line widths to one entry per segment."""
    if values is None:
        return []

    array = np.asarray(values)
    if array.size == 0:
        return []
    if array.ndim == 0:
        return [array.item()]
    return array.reshape(-1).tolist()


def draw_mesh3d(data: TikzData, obj: Line3DCollection) -> list[str]:
    """Convert a Line3DCollection into PGFPlots 3D lines."""
    content = []

    segments = getattr(obj, "_segments3d", None) or []
    colors = _normalize_color_cycle(obj.get_colors())
    linewidths = _normalize_scalar_cycle(obj.get_linewidths())
    ff = data.float_format

    for i, segment in enumerate(segments):
        points = np.asarray(segment, dtype=float)

        if points.ndim != ARRAY_DIMENSIONS or points.shape[1] != RGB_CHANNELS:
            continue

        if len(points) < MIN_SEGMENT_POINTS:
            continue

        # Preserve basic line appearance.
        options = ["no marks"]

        if colors:
            color = colors[i % len(colors)]
            pgf_color, _ = _color.mpl_color2xcolor(data, color)
            options.append(f"color={pgf_color}")

        if linewidths:
            width = linewidths[i % len(linewidths)]
            options.append(f"line width={width:{ff}}pt")

        # Each wireframe row/column becomes a 3D plot.
        content.append("\\addplot3 [" + ", ".join(options) + "] coordinates {\n")

        for x, y, z in points:
            content.append(f"({x:{ff}}, {y:{ff}}, {z:{ff}})\n")

        content.append("};\n")

    return content
