from __future__ import annotations

from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.quiver import Quiver, QuiverKey

from . import _color as mycol
from . import _files
from ._axes import _mpl_cmap2pgf_cmap
from ._util import _common_texification, get_legend_text, has_legend

if TYPE_CHECKING:
    from ._tikzdata import TikzData


@dataclass
class QuiverData:
    obj: QuiverKey


def draw_quiver_key(data: TikzData, obj: QuiverKey) -> list[str]:  # noqa: ARG001
    x = getattr(obj, "x", False)  # noqa: F841
    y = getattr(obj, "Y", False)  # noqa: F841
    u = getattr(obj, "U", False)  # noqa: F841
    angle = getattr(obj, "angle", False)  # noqa: F841
    return []


def draw_quiver(data: TikzData, obj: Quiver) -> list[str]:
    content = []
    obj.update_scalarmappable()
    obj.get_children()

    obj_xdata = obj.X
    xdata = (
        obj_xdata
        if isinstance(obj_xdata, Iterable) and isinstance(obj_xdata, Sized)
        else [obj_xdata]
    )

    if len(xdata) == 0 or obj.axes is None:
        return []

    primitive_legend = obj.axes.get_legend()
    if primitive_legend is not None and obj in primitive_legend.get_children():
        return []

    # Get several plot options
    qkey = next(
        (a for a in data.current_mpl_axes.artists if isinstance(a, QuiverKey) and obj == a.Q), None
    )
    addplot_options = _get_quiver_options(data, obj, qkey)

    legend_text = get_legend_text(obj)
    # Check if a line is in a legend and forget it if not.
    # Fixes <https://github.com/nschloe/tikzplotlib/issues/167>.
    if obj.axes is not None and has_legend(obj.axes):
        addplot_options.append("forget plot")

    # process options
    content = ["\\addplot "]
    if addplot_options:
        opts = ",\n".join(addplot_options)
        content.append(f"[\n{opts}\n]\n")

    content += _table(data, obj)

    if legend_text is not None and primitive_legend is not None:
        legend_opts = ["-stealth"]
        if obj.get_array() is None:
            legend_opts.append(_get_linecolor_quiver(data, obj))
        alpha = obj.get_alpha()
        if alpha is not None:
            legend_opts.append(f"opacity={alpha}")
        content.append(f"\\addlegendimage{{{', '.join(legend_opts)}}}\n")
        content.append(f"\\addlegendentry{{{_common_texification(legend_text)}}}\n")
    elif legend_text is not None and primitive_legend is None:
        content.append(f"\\label{{{_common_texification(legend_text) + '_plot'}}}\n")

    # get table styles

    return content


def _table(data: TikzData, obj: Quiver) -> list[str]:
    x = np.array(obj.X)
    y = np.array(obj.Y)
    udata = np.array(obj.U)
    vdata = np.array(obj.V)

    opts = []

    arrow_scaling = get_scale_units_conversion(data, obj, obj.scale_units)

    pivot_factor = 1.0 if obj.pivot == "tip" else 0.5 if obj.pivot == "middle" else 0.0
    # do the append here
    if pivot_factor != 0.0:
        opts.append(
            f"x expr={{\\thisrow{{x}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{u}}}}"
        )
        opts.append(
            f"y expr={{\\thisrow{{y}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{v}}}}"
        )

    col_sep = " "

    if data.table_row_sep != "\n":
        # don't want the \n in the table definition, just in the data (below)
        opts.append("row sep=" + data.table_row_sep.strip())

    table_row_sep = data.table_row_sep

    cdata = obj.get_array()
    has_cmap = cdata is not None

    ff = data.float_format
    if has_cmap:
        cdata = np.asarray(cdata).ravel()
        plot_table = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{col_sep}{c:{ff}}{table_row_sep}"
            for x, y, u, v, c in zip(
                x.ravel(), y.ravel(), udata.ravel(), vdata.ravel(), cdata, strict=True
            )
        ]
    else:
        plot_table = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{table_row_sep}"
            for x, y, u, v in zip(x.ravel(), y.ravel(), udata.ravel(), vdata.ravel(), strict=True)
        ]

    min_extern_length = 3

    content = []
    if data.externalize_tables and len(x) >= min_extern_length:
        filepath, rel_filepath = _files.new_filepath(data, "table", ".dat")
        with filepath.open("w") as f:
            # No encoding handling required: plot_table is only ASCII
            f.write("".join(plot_table))

        if data.externals_search_path is not None:
            esp = data.externals_search_path
            opts.append(f"search path={{{esp}}}")

        opts_str = ("[" + ",".join(opts) + "] ") if len(opts) > 0 else ""
        posix_filepath = rel_filepath.as_posix()
        content.append(f"table {{{opts_str}}}{{{posix_filepath}}};\n")
    else:
        if len(opts) > 0:
            opts_str = ",".join(opts)
            content.append(f"table [{opts_str}] {{%\n")
        else:
            content.append("table {%\n")

        if has_cmap:
            table_headers = f"x{col_sep}y{col_sep}u{col_sep}v{col_sep}colordata{table_row_sep}"
        else:
            table_headers = f"x{col_sep}y{col_sep}u{col_sep}v{table_row_sep}"
        content.extend(table_headers)
        content.extend(plot_table)
        content.append("};\n")

    return content


def _get_quiver_options(data: TikzData, obj: Quiver, qkey: QuiverKey) -> list[str]:  # noqa: ARG001
    addplot_options = []

    scale_units = obj.scale_units
    arrow_scaling = get_scale_units_conversion(data, obj, scale_units)

    # ruff: noqa: FIX002, TD002, TD003
    # TODO: fix arrow scaling, currently using hardcoded limits
    head_min_length = 0.25
    head_max_length = 1.0
    head_min_width = 0.15
    head_max_width = 0.8

    scale_arrow_head = [
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
    scale_arrow_head = "\n".join(scale_arrow_head)

    quiver_options = []
    quiver_options.append("u=\\thisrow{u},v=\\thisrow{v}")
    quiver_options.append(f"scale arrows={arrow_scaling}")
    quiver_options.append(scale_arrow_head)
    quiver_options = ",\n".join(quiver_options)

    # quiver options, including arrow and arrow head scaling
    has_cmap = obj.get_array() is not None
    if has_cmap:
        addplot_options.append("point meta=\\thisrow{colordata}")
    else:
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


def _get_linecolor_quiver(data: TikzData, obj: Quiver) -> str:
    color = obj.get_facecolors()[0]
    return mycol.mpl_color2xcolor(data, color)[0]


def get_scale_units_conversion(data: TikzData, obj: Quiver, scale_units: str | None) -> float:
    ax = data.current_mpl_axes
    fig = ax.get_figure(root=True)
    dpi = fig.dpi
    bb = ax.bbox
    dpi = fig.dpi

    fig.canvas.draw()
    unit = scale_units if obj.scale_units is not None else obj.units
    xmax, xmin = ax.get_xlim()
    ymax, ymin = ax.get_ylim()

    xlen = xmax - xmin
    ylen = ymax - ymin

    match unit:
        case "width" | None:
            scale_arrows = xlen / obj.scale
        case "height":
            scale_arrows = (ylen / bb.height) * (bb.width / xlen) * (bb.height / obj.scale)
        case "x" | "xy":
            scale_arrows = 1.0 / obj.scale
        case "y":
            scale_arrows = (1.0 / obj.scale) * (ylen / bb.height) * (bb.width / xlen)
        case "inches":
            px_per_u = dpi / obj.scale
            scale_arrows = px_per_u * (xlen / bb.width)
        case "dots":
            px_per_u = 1.0 / obj.scale
            scale_arrows = px_per_u * (xlen / bb.width)

    return abs(scale_arrows)
