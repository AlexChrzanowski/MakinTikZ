"""Convert Matplotlib 3D wireframe meshes to PGFPlots."""

import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from . import _color


def draw_mesh3d(data, obj: Line3DCollection) -> list[str]:
    """Convert a Line3DCollection into PGFPlots 3D lines."""
    content = []

    segments = obj._segments3d
    colors = obj.get_colors()
    linewidths = obj.get_linewidths()
    ff = data.float_format

    for i, segment in enumerate(segments):
        points = np.asarray(segment, dtype=float)

        if points.ndim != 2 or points.shape[1] != 3:
            continue

        if len(points) < 2:
            continue

        # Preserve basic line appearance.
        options = ["no marks"]

        if len(colors):
            color = colors[i % len(colors)]
            pgf_color, _ = _color.mpl_color2xcolor(data, color)
            options.append(f"color={pgf_color}")

        if len(linewidths):
            width = linewidths[i % len(linewidths)]
            options.append(f"line width={width:{ff}}pt")

        # Each wireframe row/column becomes a 3D plot.
        content.append(
            "\\addplot3 [" + ", ".join(options) + "] coordinates {\n"
        )

        for x, y, z in points:
            content.append(f"({x:{ff}}, {y:{ff}}, {z:{ff}})\n")

        content.append("};\n")

    return content
