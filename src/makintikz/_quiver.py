from matplotlib.quiver import Quiver, QuiverKey

from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from . import _color as mycol
from . import _files
from . import _path as mypath
from ._markers import _mpl_marker2pgfp_marker
from ._util import get_legend_text, has_legend

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

    # Get several plot options
    qkey = next(
        (a for a in data.current_mpl_axes.artists if isinstance(a, QuiverKey) and a.Q == obj), None
    )
    addplot_options = _get_quiver_options(data, obj, qkey)

    # Check if a line is in a legend and forget it if not.
    # Fixes <https://github.com/nschloe/tikzplotlib/issues/167>.
    legend_text = get_legend_text(obj)
    if legend_text is None and obj.axes is not None and has_legend(obj.axes):
        addplot_options.append("forget plot")

    # process options
    content = ["\\addplot "]
    if addplot_options:
        opts = ",\n".join(addplot_options)
        content.append(f"[\n{opts}\n]\n")

    content += _table(data, obj)

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
    # xformat = data.float_format
    col_sep = " "

    # ydata_mask = _get_ydata_mask(obj)

    if data.table_row_sep != "\n":
        # don't want the \n in the table definition, just in the data (below)
        opts.append("row sep=" + data.table_row_sep.strip())

    table_row_sep = data.table_row_sep
    # matplotlib jumps at masked or nan values, while PGFPlots by default
    # interpolates. Hence, if we have a masked plot, make sure that PGFPlots jumps
    # as well.
    # if (
    #     np.any(ydata_mask) or ~np.all(np.isfinite(ydata))
    # ) and "unbounded coords=jump" not in data.current_axis_options:
    #     data.current_axis_options.add("unbounded coords=jump")

    ff = data.float_format
    plot_table = [
        f"{x:{ff}}{col_sep}{y:{ff}}{col_sep}{u:{ff}}{col_sep}{v:{ff}}{table_row_sep}"
        for x, y, u, v in zip(X, Y, udata, vdata, strict=True)
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

        table_headers = f"x{col_sep}y{col_sep}u{col_sep}v{table_row_sep}"
        content.extend(table_headers)
        content.extend(plot_table)
        content.append("};\n")

    return content


def _get_quiver_options(data: TikzData, obj: Quiver, qkey: QuiverKey) -> list[str]:
    addplot_options = []
    line_width: str | None

        # TODO: handle line width HERE
    line_width = 0.8

    ax = data.current_mpl_axes
    xmin, xmax = ax.get_xlim()
    arrow_scaling = (xmax - xmin) / obj.scale

    # TODO: fix hardcoded values
    head_min_length = 0.25
    head_min_width = 0.20
    head_max_length = 1
    head_max_width = 1
    scale_arrow_head = [
        "every arrow/.append style={",
            f"line width={line_width}pt,",
            "   -{Stealth[",
                f"      scale length={{{head_min_length} + {head_max_length - head_min_length} * \\pgfplotspointmetatransformed / 1000}},",
                f"      scale width={{{head_min_width} + {head_max_width - head_min_width} * \\pgfplotspointmetatransformed / 1000}}",
            "   ]}",
            "}"
    ]
    scale_arrow_head = "\n".join(scale_arrow_head)

    quiver_options = []
    quiver_options.append("u=\\thisrow{u},v=\\thisrow{v}")
    quiver_options.append(f"scale arrows={arrow_scaling}")
    quiver_options.append(scale_arrow_head)
    quiver_options = ",\n".join(quiver_options)

    # quiver options, including arrow and arrow head scaling
    addplot_options.append("point meta={sqrt((\\thisrow{u})^2 + (\\thisrow{v})^2)}")
    addplot_options.append(
        f"quiver={{\n{quiver_options}}}"
    )
    addplot_options.append("-stealth")

    # if _is_errorbar_main_line(obj):
    #     ff = data.float_format
    #     line_width = f"line width={obj.get_linewidth():{ff}}pt"
    # else:
    # line_width = mypath.mpl_linewidth2pgfp_linewidth(data, line_width)
    # if line_width:
    #     addplot_options.append(line_width)
    line_xcolor = _get_linecolor_quiver(data, obj)
    addplot_options.append(line_xcolor)
    # drawstyle = _get_drawstyle_quiver(obj)
    # if drawstyle is not None:
    #     addplot_options.append(drawstyle)
    alpha = obj.get_alpha()
    if alpha is not None:
        addplot_options.append(f"opacity={alpha}")
    # linestyle = mypath.mpl_linestyle2pgfplots_linestyle(data, obj.get_linestyle(), line=obj)
    # if linestyle is not None and linestyle != "solid":
    #     addplot_options.append(linestyle)

    # marker_face_color = obj.get_markerfacecolor()
    # marker_edge_color = obj.get_markeredgecolor()

    # is_filled = marker_face_color is not None and not (
    #     isinstance(marker_face_color, str) and marker_face_color.lower() == "none"
    # )
    # mpl_marker = obj.get_marker()
    # if not isinstance(mpl_marker, str):
    #     raise NotImplementedError
    # marker, extra_mark_options = _mpl_marker2pgfp_marker(data, mpl_marker, is_filled=is_filled)
    # if marker:
    #     _marker(
    #         data,
    #         obj,
    #         MarkerData(
    #             marker=marker,
    #             mark_options=extra_mark_options,
    #             fc=marker_face_color,
    #             ec=marker_edge_color,
    #             lc=line_xcolor,
    #         ),
    #         addplot_options,
    #     )

    # if marker and linestyle is None:
    #     addplot_options.append("only marks")

    return addplot_options


def _get_linecolor_quiver(data: TikzData, obj: Quiver) -> str:
    color = obj.get_facecolors()[0]
    return mycol.mpl_color2xcolor(data, color)[0]
