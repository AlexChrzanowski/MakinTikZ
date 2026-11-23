import os
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import PIL
from matplotlib.image import AxesImage

if TYPE_CHECKING:
    from matplotlib.patches import Patch
    from matplotlib.path import Path

from . import _files, _path
from ._tikzdata import TikzData


def _save_colormap_image(
    filepath: str | os.PathLike[str], obj: AxesImage, img_array: np.ndarray
) -> None:
    """Save a colormap-based image (2D array) to file."""
    clims = obj.get_clim()
    plt.imsave(
        fname=filepath,
        arr=img_array,
        cmap=obj.get_cmap(),
        vmin=clims[0],
        vmax=clims[1],
        origin=obj.origin,
    )


def _save_rgb_image(
    filepath: str | os.PathLike[str], obj: AxesImage, img_array: np.ndarray
) -> None:
    """Save an RGB(A) image (3D array) to file."""
    dims = img_array.shape
    if not (len(dims) == 3 and dims[2] in [3, 4]):  # noqa: PLR2004
        msg = (
            "Image array should be three dimensional, with third dimension 3 (RGB) or "
            "4 (RGB+alpha) entries."
        )
        raise ValueError(msg)

    # Flip if origin is lower
    if obj.origin == "lower":
        img_array = np.flipud(img_array)

    # Convert to uint8 if needed
    img_array_uint8 = np.uint8(img_array * 255) if img_array.dtype != np.uint8 else img_array

    image = PIL.Image.fromarray(img_array_uint8)
    image.save(filepath, origin=obj.origin)


def _extract_clip_path(clip_path_obj: object) -> "Path | Patch":
    """Extract the actual clip path from matplotlib's TransformedPatchPath object."""
    if hasattr(clip_path_obj, "_patch"):
        return clip_path_obj._patch  # noqa: SLF001
    if hasattr(clip_path_obj, "get_transformed_path_and_affine"):
        clip_path, _ = clip_path_obj.get_transformed_path_and_affine()
        return clip_path
    return clip_path_obj  # type: ignore[return-value]


def draw_image(data: TikzData, obj: AxesImage) -> list[str]:
    """Returns the PGFPlots code for an image environment."""
    content = []

    filepath, rel_filepath = _files.new_filepath(data, "img", ".png")

    # Save the image to file
    img_array = obj.get_array()
    if img_array is None:
        msg = "No data in image?"
        raise ValueError(msg)

    dims = img_array.shape
    if len(dims) == 2:  # noqa: PLR2004
        _save_colormap_image(filepath, obj, img_array)
    else:
        _save_rgb_image(filepath, obj, img_array)

    # Write the corresponding TikZ code
    extent = obj.get_extent()
    if not isinstance(extent, tuple):
        extent = tuple(extent)

    ff = data.float_format
    posix_filepath = rel_filepath.as_posix()

    # Handle clip path if present
    clip_path_obj = obj.get_clip_path()
    if clip_path_obj is not None:
        content.append("\\begin{scope}\n")
        clip_path = _extract_clip_path(clip_path_obj)
        clip_command = _path.convert_clip_path(data, clip_path)
        content.append(clip_command)

    # Add the image plot command
    content.append(
        "\\addplot [forget plot] graphics [includegraphics cmd=\\pgfimage,"
        f"xmin={extent[0]:{ff}}, xmax={extent[1]:{ff}}, "
        f"ymin={extent[2]:{ff}}, ymax={extent[3]:{ff}}] {{{posix_filepath}}};\n"
    )

    if clip_path_obj is not None:
        content.append("\\end{scope}\n")

    return content
