"""Process text objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib as mpl
from matplotlib.font_manager import font_scalings
from matplotlib.patches import ArrowStyle, BoxStyle, FancyArrowPatch, FancyBboxPatch
from matplotlib.text import Annotation, Text

from . import _color

if TYPE_CHECKING:
    from ._tikzdata import TikzData


def _escape_unescaped_specials(text: str) -> str:
    """Escape &, _, % unless already escaped."""
    specials = {"&", "_", "%"}
    out: list[str] = []
    idx = 0
    while idx < len(text):
        ch = text[idx]
        if ch == "\\" and idx + 1 < len(text) and text[idx + 1] in specials:
            out.append("\\")
            out.append(text[idx + 1])
            idx += 2
            continue
        if ch in specials:
            out.append("\\")
        out.append(ch)
        idx += 1
    return "".join(out)


def _is_axes_title(obj: Text) -> bool:
    """Axes titles are handled by the axis code, not as free text."""
    axes = obj.axes
    if axes is None:
        return False
    titles = (
        axes.title,
        getattr(axes, "_left_title", None),
        getattr(axes, "_right_title", None),
    )
    return obj in titles


def _text_scaling(data: TikzData, obj: Text, *, is_figure_label: bool) -> float:
    if is_figure_label:
        # Figure-level labels should match document text size.
        return 1.0
    size = obj.get_fontsize()
    if isinstance(size, str):
        size = font_scalings[size]
    # without the factor 0.5, the fonts are too big most of the time.
    return 0.5 * size / data.font_size


_BOLD_WEIGHT_NAMES = frozenset(
    {"semibold", "demibold", "demi", "bold", "heavy", "extra bold", "black"}
)
_MIN_WEIGHT_BOLD = 550


def _is_bold(weight: str | int) -> bool:
    # get_weights returns a numeric value in the range 0-1000 or a name
    # (see matplotlib/font_manager.py)
    if isinstance(weight, int):
        return weight > _MIN_WEIGHT_BOLD
    return weight in _BOLD_WEIGHT_NAMES


def _text_style(obj: Text) -> list[str]:
    style: list[str] = []
    fontstyle = obj.get_fontstyle()
    if fontstyle == "italic":
        style.append("\\itshape")
    elif fontstyle != "normal":
        msg = f"Object style '{fontstyle}' not implemented."
        raise NotImplementedError(msg)
    if _is_bold(obj.get_fontweight()):
        style.append("\\bfseries")
    return style


def draw_text(data: TikzData, obj: Text) -> list[str]:
    """Paints text on the graph.

    :return: Content for tikz plot.
    """
    content: list[str] = []
    properties: list[str] = []
    style: list[str] = []
    ff = data.float_format
    tikz_pos = _get_tikz_pos(data, obj, content)

    placement = _figure_label_placement(obj)
    if placement is not None:
        bbox_side, _node_anchor, (dx, dy) = placement
        gap = _FIGURE_LABEL_GAP_PT
        tikz_pos = f"($(current bounding box.{bbox_side})+({dx * gap:{ff}}pt,{dy * gap:{ff}}pt)$)"

    text = obj.get_text()

    if _is_axes_title(obj) or text == "":
        return content

    size = obj.get_fontsize()
    if isinstance(size, str):
        size = font_scalings[size]
    bbox = obj.get_bbox_patch()
    converter = mpl.colors.ColorConverter()

    scaling = _text_scaling(data, obj, is_figure_label=placement is not None)
    if scaling != 1.0:
        properties.append(f"scale={scaling:{ff}}")

    if bbox is not None:
        _bbox(data, bbox, properties, scaling)

    ha = obj.get_horizontalalignment()
    va = obj.get_verticalalignment()
    anchor = f"anchor={placement[1]}" if placement else _transform_positioning(ha, va)
    if anchor:
        properties.append(anchor)
    col, _ = _color.mpl_color2xcolor(data, converter.to_rgb(obj.get_color()))
    properties.append(f"text={col}")
    properties.append(f"rotate={obj.get_rotation():.1f}")

    style = _text_style(obj)

    text = _escape_unescaped_specials(text)

    if "\n" in text:
        # http://tex.stackexchange.com/a/124114/13262
        properties.append(f"align={ha}")
        # Manipulating the text here is actually against mpl2tikz's policy not
        # to do that. On the other hand, newlines should translate into
        # newlines.
        # We might want to remove this here in the future.
        text = text.replace("\n", "\\\\")

    props = ",\n  ".join(properties)
    text = " ".join([*style, text])
    content.append(f"\\draw {tikz_pos} node[\n  {props}\n]{{{text}}};\n")
    return content


def _get_tikz_pos(data: TikzData, obj: Text, content: list[str]) -> str:
    """Gets the position in tikz format."""
    pos = _annotation(data, obj, content) if isinstance(obj, Annotation) else obj.get_position()

    if isinstance(pos, str):
        return pos
    if obj.axes:
        # Check if the text uses axes-relative coordinates (transform=ax.transAxes).
        # In that case, use `rel axis cs` instead of `axis cs`.
        transform = obj.get_transform()
        if transform == obj.axes.transAxes:
            return f"(rel axis cs:{pos[0]:{data.float_format}},{pos[1]:{data.float_format}})"
        return f"(axis cs:{pos[0]:{data.float_format}},{pos[1]:{data.float_format}})"
    # relative to the entire figure, it's a getting a littler harder. See
    # <http://tex.stackexchange.com/a/274902/13262> for a solution to the
    # problem:
    return (
        f"({{$(current bounding box.south west)!{pos[0]:{data.float_format}}!"
        "(current bounding box.south east)$}"
        "|-"
        f"{{$(current bounding box.south west)!{pos[1]:{data.float_format}}!"
        "(current bounding box.north west)$})"
    )


def _transform_positioning(horizontal_alignment: str, vertical_aligment: str) -> str:
    """Converts matplotlib positioning to pgf node positioning.

    Not quite accurate but the results are equivalent more or less.
    """
    if horizontal_alignment == "center" and vertical_aligment == "center":
        return ""

    ha_mpl_to_tikz = {"right": "east", "left": "west", "center": ""}
    va_mpl_to_tikz = {"top": "north", "bottom": "south", "center": "", "baseline": "base"}
    anchor = " ".join(
        [va_mpl_to_tikz[vertical_aligment], ha_mpl_to_tikz[horizontal_alignment]]
    ).strip()
    return f"anchor={anchor}"


def _parse_annotation_coords(float_format: str, coords: str, xy: tuple[float, float]) -> str:
    """Convert a coordinate name and xy into a tikz coordinate string."""
    if coords == "data":
        x, y = xy
        return f"(axis cs:{x:{float_format}},{y:{float_format}})"
    if coords in [
        "figure points",
        "figure pixels",
        "figure fraction",
        "axes points",
        "axes pixels",
        "axes fraction",
        "data",
        "polar",
    ]:
        raise NotImplementedError
    # unknown
    raise NotImplementedError


def _get_arrow_style(data: TikzData, obj: FancyArrowPatch) -> list:
    # get a style string from a FancyArrowPatch
    arrow_translate = {
        "-": ["-"],
        "->": ["->"],
        "<-": ["<-"],
        "<->": ["<->"],
        "<|-": ["latex-"],
        "-|>": ["-latex"],
        "<|-|>": ["latex-latex"],
        "]-": ["|-"],
        "-[": ["-|"],
        "]-[": ["|-|"],
        "|-|": ["|-|"],
        "]->": ["]->"],
        "<-[": ["<-["],
        "simple": ["-latex", "very thick"],
        "fancy": ["-latex", "very thick"],
        "wedge": ["-latex", "very thick"],
    }
    style_cls = type(obj.get_arrowstyle())

    # Sometimes, mpl adds new arrow styles to the ArrowStyle._style_list dictionary.
    # To support multiple mpl versions, check in a loop instead of a dictionary lookup.
    latex_style = None
    for key, value in arrow_translate.items():
        if key not in ArrowStyle._style_list:  # type: ignore[attr-defined]  # noqa: SLF001  (there is no other way; not all ArrowStyle contain the .arrow attribute)
            continue

        if ArrowStyle._style_list[key] == style_cls:  # type: ignore[attr-defined]  # noqa: SLF001
            latex_style = value
            break

    if latex_style is None:
        msg = f"Unknown arrow style {style_cls}"
        raise NotImplementedError(msg)

    col, _ = _color.mpl_color2xcolor(data, obj.get_edgecolor())
    return [*latex_style, "draw=" + col]


def _annotation(data: TikzData, obj: Annotation, content: list[str]) -> str | tuple[float, float]:
    ann_xy = obj.xy
    ann_xycoords = obj.xycoords
    if not isinstance(ann_xycoords, str):
        # Anything else except for explicit positioning is not supported yet
        return obj.get_position()
    ann_xytext = obj.xyann
    ann_textcoords = obj.anncoords

    ff = data.float_format

    try:
        xy_pos = _parse_annotation_coords(ff, ann_xycoords, ann_xy)
    except NotImplementedError:
        # Anything else except for explicit positioning is not supported yet
        return obj.get_position()

    # special cases only for text_coords
    if ann_textcoords == "offset points":
        x, y = ann_xytext
        unit = "pt"
        text_pos = f"{xy_pos} ++({x:{ff}}{unit},{y:{ff}}{unit})"
    else:
        try:
            text_pos = _parse_annotation_coords(ff, ann_xycoords, ann_xytext)
        except NotImplementedError:
            # Anything else except for explicit positioning is not supported yet
            return obj.get_position()

    if obj.arrow_patch:
        style = ",".join(_get_arrow_style(data, obj.arrow_patch))
        the_arrow = f"\\draw[{style}] {text_pos} -- {xy_pos};\n"
        content.append(the_arrow)
    return text_pos


# name on Figure -> (default position, bbox side, node anchor, outward direction)
_FIGURE_LABELS = {
    "_suptitle": ((0.5, 0.98), "north", "south", (0, 1)),
}
_FIGURE_LABEL_GAP_PT = 4.0


def _figure_label_placement(obj: Text) -> tuple[str, str, tuple[int, int]] | None:
    """Detect fig.suptitle at their automatic position.

    Returns (bbox side, node anchor, outward direction) or None.
    """
    fig = obj.figure
    if fig is None:
        return None
    for attr, (default, bbox_side, node_anchor, direction) in _FIGURE_LABELS.items():
        if obj is not getattr(fig, attr, None):
            continue
        pos = obj.get_position()
        # `_autopos` is set by mpl when x/y were not given (layout engines may
        # then move the text), so fall back to comparing with the defaults.
        nearly_zero = 1e-9
        at_default = getattr(obj, "_autopos", False) or all(
            abs(a - b) < nearly_zero for a, b in zip(pos, default, strict=True)
        )
        if not at_default:
            return None  # user chose a custom position: keep existing behavior
        return bbox_side, node_anchor, direction
    return None


def _bbox(data: TikzData, bbox: FancyBboxPatch, properties: list[str], scaling: float) -> None:
    bbox_style = bbox.get_boxstyle()
    if bbox.get_fill():
        facecolor, _ = _color.mpl_color2xcolor(data, bbox.get_facecolor())
        if facecolor:
            properties.append(f"fill={facecolor}")
    edgecolor, _ = _color.mpl_color2xcolor(data, bbox.get_edgecolor())
    if edgecolor:
        properties.append(f"draw={edgecolor}")
    ff = data.float_format
    line_width = bbox.get_linewidth() * 0.4
    properties.append(f"line width={line_width:{ff}}pt")
    inner_sep = bbox_style.pad * data.font_size  # type: ignore[attr-defined]
    properties.append(f"inner sep={inner_sep:{ff}}pt")
    if bbox.get_alpha():
        properties.append(f"fill opacity={bbox.get_alpha()}")

    # Process the style and linestyle of the bounding box.
    _bbox_style(data, bbox_style, properties)
    _bbox_linestyle(bbox, properties, scaling)


def _bbox_style(
    data: TikzData,
    bbox_style: BoxStyle
    | BoxStyle.Round
    | BoxStyle.RArrow
    | BoxStyle.LArrow
    | BoxStyle.DArrow
    | BoxStyle.Circle
    | BoxStyle.Roundtooth
    | BoxStyle.Sawtooth
    | BoxStyle.Square,
    properties: list[str],
) -> None:
    if isinstance(bbox_style, BoxStyle.Round):
        properties.append("rounded corners")
    elif isinstance(bbox_style, BoxStyle.RArrow):
        data.tikz_libs.add("shapes.arrows")
        properties.append("single arrow")
    elif isinstance(bbox_style, BoxStyle.LArrow):
        data.tikz_libs.add("shapes.arrows")
        properties.append("single arrow")
        properties.append("shape border rotate=180")
    elif isinstance(bbox_style, BoxStyle.DArrow):
        data.tikz_libs.add("shapes.arrows")
        properties.append("double arrow")
    elif isinstance(bbox_style, BoxStyle.Circle):
        properties.append("circle")
    elif isinstance(bbox_style, BoxStyle.Roundtooth):
        properties.append("decorate")
        properties.append("decoration={snake,amplitude=0.5,segment length=3}")
    elif isinstance(bbox_style, BoxStyle.Sawtooth):
        properties.append("decorate")
        properties.append("decoration={zigzag,amplitude=0.5,segment length=3}")
    elif not isinstance(bbox_style, BoxStyle.Square):
        msg = f"bbox_style '{type(bbox_style)}' not implemented."
        raise NotImplementedError(msg)


def _bbox_linestyle(bbox: FancyBboxPatch, properties: list[str], scaling: float) -> None:
    bbox_ls = bbox.get_linestyle()
    if bbox_ls == "dotted":
        properties.append("dotted")
    elif bbox_ls == "dashed":
        properties.append("dashed")
    elif bbox_ls == "dashdot":
        s1 = 1.0 / scaling
        s3 = 3.0 / scaling
        s6 = 6.0 / scaling
        properties.append(f"dash pattern=on {s1:.3g}pt off {s3:.3g}pt on {s6:.3g}pt off {s3:.3g}pt")
    elif bbox_ls != "solid":
        msg = f"bbox line style '{bbox_ls}' not implemented."
        raise NotImplementedError(msg)
