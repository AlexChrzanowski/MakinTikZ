from __future__ import annotations

from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeGuard

import numpy as np
from matplotlib.figure import Figure
from matplotlib.quiver import Quiver, QuiverKey
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from . import _color as mycol
from . import _files
from ._axes import _mpl_cmap2pgf_cmap
from ._util import _common_texification, get_legend_text, has_legend

if TYPE_CHECKING:
    from ._tikzdata import TikzData

QuiverArtist = Quiver | Line3DCollection

MIN_EXTERN_LENGTH = 3
DOT_TOLERANCE = 1e-12
SYMMETRY_TOLERANCE = 1e-6


@dataclass
class QuiverData:
    obj: QuiverKey


def draw_quiver_key(data: TikzData, obj: QuiverKey) -> list[str]:  # noqa: ARG001
    x = getattr(obj, "x", False)  # noqa: F841
    y = getattr(obj, "Y", False)  # noqa: F841
    u = getattr(obj, "U", False)  # noqa: F841
    angle = getattr(obj, "angle", False)  # noqa: F841
    return []


def _is_empty_quiver(obj: QuiverArtist, *, is_3d: bool) -> bool:
    if is_3d:
        return len(obj._segments3d) == 0  # type: ignore[union-attr]  # noqa: SLF001

    obj_xdata = obj.X  # type: ignore[union-attr]
    xdata = (
        obj_xdata
        if isinstance(obj_xdata, Iterable) and isinstance(obj_xdata, Sized)
        else [obj_xdata]
    )
    return len(xdata) == 0


def _append_quiver_legend(
    data: TikzData, obj: QuiverArtist, legend_text: str | None, primitive_legend: object
) -> list[str]:
    if legend_text is None:
        return []
    if primitive_legend is not None:
        legend_opts = ["-stealth"]
        if obj.get_array() is None:
            legend_opts.append(_get_linecolor_quiver(data, obj))
        alpha = obj.get_alpha()
        if alpha is not None:
            legend_opts.append(f"opacity={alpha}")
        return [
            f"\\addlegendimage{{{', '.join(legend_opts)}}}\n",
            f"\\addlegendentry{{{_common_texification(legend_text)}}}\n",
        ]
    return [f"\\label{{{_common_texification(legend_text) + '_plot'}}}\n"]


def draw_quiver(data: TikzData, obj: QuiverArtist) -> list[str]:
    obj.update_scalarmappable()
    obj.get_children()

    is_3d = is_3d_quiver(obj)
    if obj.axes is None or data.current_mpl_axes is None or _is_empty_quiver(obj, is_3d=is_3d):
        return []

    primitive_legend = obj.axes.get_legend()
    if primitive_legend is not None and obj in primitive_legend.get_children():
        return []

    qkey = next(
        (a for a in data.current_mpl_axes.artists if isinstance(a, QuiverKey) and obj == a.Q), None
    )
    addplot_options = _get_quiver_options(data, obj, qkey)

    legend_text = get_legend_text(obj)
    # Check if a line is in a legend and forget it if not.
    # Fixes <https://github.com/nschloe/tikzplotlib/issues/167>.
    if has_legend(obj.axes):
        addplot_options.append("forget plot")

    content = ["\\addplot3 "] if is_3d else ["\\addplot "]
    if addplot_options:
        opts = ",\n".join(addplot_options)
        content.append(f"[\n{opts}\n]\n")

    content += _table(data, obj)
    content += _append_quiver_legend(data, obj, legend_text, primitive_legend)
    return content


def _process_3d_table(
    data: TikzData, obj: Line3DCollection, cdata: np.ndarray | None
) -> tuple[str, list[str], list[str], int]:
    col_sep = " "
    sep = data.table_row_sep
    ff = data.float_format
    x, y, z, udata, vdata, wdata = _extract_3d_quiver_vectors(obj)

    if cdata is not None:
        cdata_flat = np.asarray(cdata).ravel()
        headers = f"x{col_sep}y{col_sep}z{col_sep}u{col_sep}v{col_sep}w{col_sep}colordata{sep}"
        rows = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{z:{ff}}{col_sep}"
            f"{u:{ff}}{col_sep}{v:{ff}}{col_sep}{w:{ff}}{col_sep}{ci:{ff}}{sep}"
            for x, y, z, u, v, w, ci in zip(
                x.ravel(),
                y.ravel(),
                z.ravel(),
                udata.ravel(),
                vdata.ravel(),
                wdata.ravel(),
                cdata_flat,
                strict=True,
            )
        ]
    else:
        headers = f"x{col_sep}y{col_sep}z{col_sep}u{col_sep}v{col_sep}w{sep}"
        rows = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{z:{ff}}{col_sep}"
            f"{u:{ff}}{col_sep}{v:{ff}}{col_sep}{w:{ff}}{sep}"
            for x, y, z, u, v, w in zip(
                x.ravel(),
                y.ravel(),
                z.ravel(),
                udata.ravel(),
                vdata.ravel(),
                wdata.ravel(),
                strict=True,
            )
        ]

    return headers, rows, [], x.size


def _process_2d_table(
    data: TikzData, obj: Quiver, cdata: np.ndarray | None
) -> tuple[str, list[str], list[str], int]:
    col_sep = " "
    sep = data.table_row_sep
    ff = data.float_format
    opts: list[str] = []

    x = np.array(obj.X)
    y = np.array(obj.Y)
    udata = np.array(obj.U)
    vdata = np.array(obj.V)

    arrow_scaling = get_scale_units_conversion(data, obj, obj.scale_units)
    pivot_factor = 1.0 if obj.pivot == "tip" else 0.5 if obj.pivot == "middle" else 0.0
    if pivot_factor != 0.0:
        opts.append(
            f"x expr={{\\thisrow{{x}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{u}}}}"
        )
        opts.append(
            f"y expr={{\\thisrow{{y}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{v}}}}"
        )

    if cdata is not None:
        cdata_flat = np.asarray(cdata).ravel()
        headers = f"x{col_sep}y{col_sep}u{col_sep}v{col_sep}colordata{sep}"
        rows = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{col_sep}{cdata_flat[i]:{ff}}{sep}"
            for i, (x, y, u, v) in enumerate(
                zip(x.ravel(), y.ravel(), udata.ravel(), vdata.ravel(), strict=True)
            )
        ]
    else:
        headers = f"x{col_sep}y{col_sep}u{col_sep}v{sep}"
        rows = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{sep}"
            for x, y, u, v in zip(x.ravel(), y.ravel(), udata.ravel(), vdata.ravel(), strict=True)
        ]

    return headers, rows, opts, x.size


def _table(data: TikzData, obj: QuiverArtist) -> list[str]:
    cdata = obj.get_array()
    if is_3d_quiver(obj):
        table_headers, plot_table, opts, n_arrows = _process_3d_table(data, obj, cdata)
    else:
        table_headers, plot_table, opts, n_arrows = _process_2d_table(data, obj, cdata)

    if data.table_row_sep != "\n":
        opts.append("row sep=" + data.table_row_sep.strip())

    content = []
    if data.externalize_tables and n_arrows >= MIN_EXTERN_LENGTH:
        filepath, rel_filepath = _files.new_filepath(data, "table", ".dat")
        with filepath.open("w") as f:
            f.write(table_headers)
            f.write("".join(plot_table))

        if data.externals_search_path is not None:
            esp = data.externals_search_path
            opts.append(f"search path={{{esp}}}")

        opts_str = ("[" + ",".join(opts) + "] ") if opts else ""
        posix_filepath = rel_filepath.as_posix()
        content.append(f"table {{{opts_str}}}{{{posix_filepath}}};\n")
    else:
        if opts:
            opts_str = ",".join(opts)
            content.append(f"table [{opts_str}] {{%\n")
        else:
            content.append("table {%\n")

        content.append(table_headers)
        content.extend(plot_table)
        content.append("};\n")

    return content


def _get_quiver_options(data: TikzData, obj: QuiverArtist, qkey: QuiverKey | None) -> list[str]:  # noqa: ARG001
    # qkey argument is currently unused
    # qkey still needs to be implemented

    addplot_options = []

    if not is_3d_quiver(obj):
        scale_units = obj.scale_units
        arrow_scaling = get_scale_units_conversion(data, obj, scale_units)

        # ruff: noqa: FIX002, TD002, TD003
        # TODO: fix arrow scaling, currently using hardcoded limits
        head_min_length = 0.25
        head_max_length = 1.0
        head_min_width = 0.15
        head_max_width = 0.8

        scale_arrow_head_lines = [
            "every arrow/.append style={",
            "    -{Stealth[",
            (
                f"      scale length={{{head_min_length} + {head_max_length}"
                " * \\pgfplotspointmetatransformed / 1000},"
            ),
            (
                f"      scale width={{{head_min_width} + {head_max_width}"
                " * \\pgfplotspointmetatransformed / 1000}"
            ),
            "    ]}",
            "}",
        ]
        scale_arrow_head = "\n".join(scale_arrow_head_lines)

        quiver_options_list = [
            "u=\\thisrow{u},v=\\thisrow{v}",
            f"scale arrows={arrow_scaling}",
            scale_arrow_head,
        ]
        quiver_options = ",\n".join(quiver_options_list)
    else:
        quiver_options = (
            "u=\\thisrow{u},v=\\thisrow{v},w=\\thisrow{w},\nevery arrow/.append style={-stealth}"
        )

    # quiver options, including arrow and arrow head scaling
    has_cmap = obj.get_array() is not None
    if has_cmap:
        addplot_options.append("point meta=\\thisrow{colordata}")
    elif not is_3d_quiver(obj):
        addplot_options.append("point meta={sqrt((\\thisrow{u})^2 + (\\thisrow{v})^2)}")

    addplot_options.append(f"quiver={{\n{quiver_options}}}")

    if has_cmap and obj.get_cmap():
        mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap(obj.get_cmap(), data)
        addplot_options.append("colormap" + ("=" if is_custom_cmap else "/") + mycolormap)
        if obj.norm is not None:
            if obj.norm.vmin is not None:
                addplot_options.append(f"point meta min={obj.norm.vmin:{data.float_format}}")
            if obj.norm.vmax is not None:
                addplot_options.append(f"point meta max={obj.norm.vmax:{data.float_format}}")
        addplot_options.append("quiver/every arrow/.append style={color=mapped color}")
    else:
        line_xcolor = _get_linecolor_quiver(data, obj)
        addplot_options.append(line_xcolor)

    alpha = obj.get_alpha()
    if alpha is not None:
        addplot_options.append(f"opacity={alpha}")

    return addplot_options


def _get_linecolor_quiver(data: TikzData, obj: QuiverArtist) -> str:
    colors = obj.get_edgecolor() if is_3d_quiver(obj) else obj.get_facecolor()
    color = colors[0]
    if isinstance(color, float):
        color = (color, color, color)
    return mycol.mpl_color2xcolor(data, color)[0]


def get_scale_units_conversion(data: TikzData, obj: Quiver, scale_units: str | None) -> float:
    ax = data.current_mpl_axes
    if ax is None:
        return 1.0

    fig = ax.get_figure()
    while (
        fig is not None
        and (parent := getattr(fig, "figure", None)) is not None
        and parent is not fig
    ):
        fig = parent
    if not isinstance(fig, Figure):
        return 1.0

    dpi = fig.dpi
    bb = ax.bbox

    fig.canvas.draw()
    unit = scale_units if obj.scale_units is not None else obj.units
    xmax, xmin = ax.get_xlim()
    ymax, ymin = ax.get_ylim()

    xlen = xmax - xmin
    ylen = ymax - ymin
    scale = obj.scale if obj.scale is not None else 1.0

    match unit:
        case "width" | None:
            scale_arrows = xlen / scale
        case "height":
            scale_arrows = (ylen / bb.height) * (bb.width / xlen) * (bb.height / scale)
        case "x" | "xy":
            scale_arrows = 1.0 / scale
        case "y":
            scale_arrows = (1.0 / scale) * (ylen / bb.height) * (bb.width / xlen)
        case "inches":
            px_per_u = dpi / scale
            scale_arrows = px_per_u * (xlen / bb.width)
        case "dots":
            px_per_u = 1.0 / scale
            scale_arrows = px_per_u * (xlen / bb.width)

    return abs(scale_arrows)


def is_3d_quiver(obj: object) -> TypeGuard[Line3DCollection]:
    """Return True if obj is a Line3DCollection representing a 3D quiver plot."""
    return (
        isinstance(obj, Line3DCollection)
        and getattr(obj.axes, "name", None) == "3d"
        and hasattr(obj, "_segments3d")
    )


def _has_3d_quiver_arrowheads(segments: np.ndarray) -> bool:
    """Verify whether segments[N:3N] are Matplotlib 3D quiver arrowhead barbs."""
    n_total = len(segments)
    segments_per_arrow = 3
    if n_total < segments_per_arrow or n_total % segments_per_arrow != 0:
        return False

    n = n_total // segments_per_arrow
    # Matplotlib 3D quiver stores shafts as [tip, tail]
    tips = segments[:n, 0, :]
    tails = segments[:n, 1, :]
    shafts = tips - tails  # direction vector from tail -> tip

    barb1_starts = segments[n : 2 * n, 0, :]
    barb2_starts = segments[2 * n :, 0, :]

    # 1. Both barbs for arrow i originate at tip i (index 0)
    if not (np.allclose(tips, barb1_starts) and np.allclose(tips, barb2_starts)):
        return False

    barb1 = segments[n : 2 * n, 1, :] - tips
    barb2 = segments[2 * n :, 1, :] - tips

    # 2. Both barbs must have equal length
    len1 = np.linalg.norm(barb1, axis=1)
    len2 = np.linalg.norm(barb2, axis=1)
    if not np.allclose(len1, len2):
        return False

    # 3. Barbs must point backward against the shaft (dot product <= 0)
    dot1 = np.einsum("ij,ij->i", barb1, shafts)
    dot2 = np.einsum("ij,ij->i", barb2, shafts)
    if not (np.all(dot1 <= DOT_TOLERANCE) and np.all(dot2 <= DOT_TOLERANCE)):
        return False

    # 4. Barbs must be symmetric around the shaft axis: (barb1 + barb2) x shaft == 0
    cross = np.cross(barb1 + barb2, shafts)
    shaft_lens = np.linalg.norm(shafts, axis=1)
    barb_sum_lens = np.linalg.norm(barb1 + barb2, axis=1)
    scale = np.maximum(shaft_lens * barb_sum_lens, 1.0)
    return bool(np.all(np.linalg.norm(cross, axis=1) / scale < SYMMETRY_TOLERANCE))


def _get_3d_quiver_arrow_count(obj: Line3DCollection, segments: np.ndarray) -> int:
    """Definitively determine N (number of arrows) in a 3D quiver Line3DCollection."""
    n_total = len(segments)
    if n_total == 0:
        return 0

    # 1. Definitive: scalar colormap array always has 1 entry per arrow (N)
    cdata = obj.get_array()
    if cdata is not None and len(cdata) > 0:
        return len(cdata)

    # 2. Definitive: explicit per-arrow styling arrays of length N (when N > 1)
    for prop in (obj.get_edgecolor(), obj.get_linewidths(), obj.get_linestyles()):
        if len(prop) > 1 and len(prop) < n_total:
            return len(prop)

    # 3. Fallback for uniform-styled arrows: check if segments[N:3N] are symmetric backward barbs
    if _has_3d_quiver_arrowheads(segments):
        return n_total // 3

    return n_total


def _extract_3d_quiver_vectors(
    obj: Line3DCollection,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Extract (x, y, z, u, v, w) shaft vectors from a 3D quiver Line3DCollection."""
    segments = np.asarray(obj._segments3d, dtype=float)  # noqa: SLF001
    n_arrows = _get_3d_quiver_arrow_count(obj, segments)
    if n_arrows == 0:
        empty = np.array([], dtype=float)
        return empty, empty, empty, empty, empty, empty

    shafts = segments[:n_arrows]  # shape: (N, 2, 3), stored as [tip, tail]
    tips = shafts[:, 0, :]
    tails = shafts[:, 1, :]
    deltas = tips - tails
    return (
        tails[:, 0],
        tails[:, 1],
        tails[:, 2],
        deltas[:, 0],
        deltas[:, 1],
        deltas[:, 2],
    )
