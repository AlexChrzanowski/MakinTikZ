"""Export simple Matplotlib 3D bars as PGFPlots polygon patches."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import numpy as np

from . import _color

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

if TYPE_CHECKING:
    from ._tikzdata import TikzData


def draw_bar3d(data: TikzData, obj: Poly3DCollection) -> list[str]:
    """Export rectangular 3D faces as one solid-color PGFPlots patch plot.

    Initial scope: uniform face color, four-vertex rectangular faces.
    Matplotlib's internal 3D vertex representation is currently private.
    """
    vertices_per_face = 4
    coordinate_dimensions = 3

    # Matplotlib 3.11+ stores polygon coordinates in _faces.
    raw_faces = getattr(obj, "_faces", None)

    if raw_faces is not None:
        faces = np.asarray(raw_faces, dtype=float)
    else:
        # Compatibility with older Matplotlib versions.
        vertices = getattr(obj, "_vec", None)
        face_slices = getattr(obj, "_segslices", None)
        if vertices is None or face_slices is None:
            warnings.warn(
                "3D polygon vertices are unavailable; skipping collection.",
                stacklevel=2,
            )
            return []

        faces = np.asarray(
            [np.asarray(vertices[:3, face_slice], dtype=float).T for face_slice in face_slices],
            dtype=float,
        )

    expected_dimensions = 3
    if faces.ndim != expected_dimensions or faces.shape[1:] != (
        vertices_per_face,
        coordinate_dimensions,
    ):
        warnings.warn(
            "Only four-corner 3D polygon faces are supported.",
            stacklevel=2,
        )
        return []

    if not np.all(np.isfinite(faces)):
        warnings.warn(
            "3D polygon faces contain invalid coordinates.",
            stacklevel=2,
        )
        return []

    if len(faces) == 0:
        return []

    # When shade=False and a single color is passed to bar3d, these are equal.
    facecolors = np.asarray(getattr(obj, "_facecolor3d", obj.get_facecolors()))
    if len(facecolors) == 0 or not np.allclose(facecolors, facecolors[0]):
        warnings.warn(
            "This initial 3D bar exporter supports only a single unshaded color; "
            "use ax.bar3d(..., shade=False, color='blue').",
            stacklevel=2,
        )
        return []

    color, _ = _color.mpl_color2xcolor(data, facecolors[0])
    ff = data.float_format
    output = [
        f"\\addplot3 [patch, patch type=rectangle, fill={color}, "
        "draw=black, shader=flat, forget plot] coordinates {\n"
    ]
    for face in faces:
        for x, y, z in face:
            output.append(f"({x:{ff}}, {y:{ff}}, {z:{ff}})\n")
    output.append("};\n")
    return output
