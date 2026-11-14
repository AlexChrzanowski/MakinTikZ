from __future__ import annotations

from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
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


def draw_quiver_key(data: TikzData, obj: QuiverKey) -> list[str]:
    X = getattr(obj, "X", False)
    Y = getattr(obj, "Y", False)
    U = getattr(obj, "U", False)
    angle = getattr(obj, "angle", False)
    return []


def _get_arrow_scaling(ax: plt.Axes, obj: Quiver) -> float:
    if obj.scale is None and ax.figure is not None:
        ax.figure.canvas.draw()
    scale = obj.scale if obj.scale is not None else 1.0
    xmin, xmax = ax.get_xlim()
    return (xmax - xmin) / scale


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
    X = obj.X
    Y = obj.Y
    U = obj.U
    V = obj.V

    X = np.array(X)
    Y = np.array(Y)
    udata = np.array(U)
    vdata = np.array(V)

    opts = []

    ax = data.current_mpl_axes
    arrow_scaling = _get_arrow_scaling(ax, obj)
    pivot_factor = 1.0 if obj.pivot == "tip" else 0.5 if obj.pivot == "middle" else 0.0
    # do the append here
    if pivot_factor != 0.0:
        opts.append(
            f"x expr={{\\thisrow{{x}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{u}}}}"
        )
        opts.append(
            f"y expr={{\\thisrow{{y}} - {pivot_factor} * {arrow_scaling} * \\thisrow{{v}}}}"
        )

    # xformat = data.float_format
    col_sep = " "

    # ydata_mask = _get_ydata_mask(obj)

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
                X.ravel(), Y.ravel(), udata.ravel(), vdata.ravel(), cdata, strict=True
            )
        ]
    else:
        plot_table = [
            f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{table_row_sep}"
            for x, y, u, v in zip(X.ravel(), Y.ravel(), udata.ravel(), vdata.ravel(), strict=True)
        ]

    min_extern_length = 3

    content = []
    if data.externalize_tables and len(X) >= min_extern_length:
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


def _get_quiver_options(data: TikzData, obj: Quiver, qkey: QuiverKey) -> list[str]:
    addplot_options = []
    line_width: str | None

    ax = data.current_mpl_axes
    xmin, xmax = ax.get_xlim()
    arrow_scaling = _get_arrow_scaling(ax, obj)
    units = obj.units

    fig = ax.figure
    axes_width_in = ax.bbox.width / fig.dpi

    match units:
        case "width":
            arrow_scaling = _get_arrow_scaling(ax, obj)
        case _:
            arrow_scaling = 100

    line_width = obj.width * axes_width_in

    print(obj.span)

    head_min_length = 0.15 * (obj.headlength / 5.0)
    head_max_length = 1.0 * (obj.headlength / 5.0)
    head_min_width = 0.25 * (obj.headwidth / 3.0)
    head_max_width = 1.0 * (obj.headwidth / 3.0)
    scale_arrow_head = [
        "every arrow/.append style={",
        f"line width={line_width}pt,",
        "   -{Stealth[",
        f"      scale length={{{head_min_length} + {head_max_length - head_min_length} * \\pgfplotspointmetatransformed / 1000}},",
        f"      scale width={{{head_min_width} + {head_max_width - head_min_width} * \\pgfplotspointmetatransformed / 1000}}",
        "   ]}",
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
