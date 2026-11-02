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
    return []