from typing import Dict, Any
from functools import lru_cache

import reflex as rx
from reflex import Component, Var, NoSSRComponent

from reflex.components.el import Div


class GridLayoutBase(NoSSRComponent):
    library = 'react-grid-layout'

#     @staticmethod
#     @lru_cache(maxsize=None)
#     def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
#         return {
#             (160, "GridLayoutWidthProvider"): width_provider,
#         }
#
#
# class WidthProvider(GridLayoutBase):
#     tag = "WidthProvider"
#     alias = "GridLayoutWidthProvider"
#
#
# width_provider = WidthProvider.create()
#


class GridLayout(GridLayoutBase):
    tag = "GridLayout"
    is_default = True
    cols: Var[int]
    width: Var[int]
    rowHeight: Var[int]
    autoSize: Var[bool]


class ResponsiveGridLayout(GridLayoutBase):
    tag = "Responsive"
    alias = "ResponsiveGridLayout"


class GridLayoutItem(Div):
    data_grid: Var[Dict[str, Any]]


grid_layout = GridLayout.create
responsive_grid_layout = ResponsiveGridLayout.create
grid_layout_item = GridLayoutItem.create
