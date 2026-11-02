from matplotlib.quiver import QuiverKey

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matplotlib.collections import LineCollection
    from matplotlib.lines import Line2D

    from ._tikzdata import TikzData

@dataclass
class QuiverData:
    obj: QuiverKey

def draw_arrow(data: TikzData, obj: QuiverKey) -> list[str]:
    print(obj)
    X = getattr(obj, "X", False)
    Y = getattr(obj, "Y", False)
    U = getattr(obj, "U", False)
    angle = getattr(obj, "angle", False)

    quiver_options = _get_quiver_options(data, obj)

    content = ["\\addplot "]
    if quiver_options:
        opts = ", ".join(quiver_options)
        content.append(f"[{opts}]\n")
        
    return []

def _get_quiver_options(data: TikzData, obj: QuiverKey) -> list[str]:
    # TODO: rename to match PGFPlots command
    quiver_options = []
    return quiver_options