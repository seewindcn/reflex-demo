from typing import Dict, Any, List
from functools import lru_cache

import reflex as rx
from reflex import Component, Var, NoSSRComponent

from reflex.components.el import Div
from reflex.utils import imports


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
    cols: Var[int] = 12
    width: Var[int]
    row_height: Var[int]
    auto_size: Var[bool]


class ResponsiveGridLayout(GridLayoutBase):
    tag = "ResponsiveGridLayout"
    cols: Var[Dict[str, int]] = dict(lg=12, md=10, sm=6, xs=4, xxs=2)
    breakpoints: Var[Dict[str, int]] = dict(lg=1200, md=996, sm=768, xs=480, xxs=0)
    row_height: Var[int]
    auto_size: Var[bool]

    def _get_imports(self) -> imports.ImportDict:
        return imports.merge_imports(
            # super()._get_imports(),
            {self.library: {imports.ImportVar(tag='WidthProvider'), imports.ImportVar(tag='Responsive'), }},
        )

    def _get_dynamic_imports(self) -> str:
        return ""

    def _get_custom_code(self) -> str | None:
        return "const ResponsiveGridLayout = WidthProvider(Responsive);"


class GridLayoutItem(Div):
    data_grid: Var[Dict[str, Any]]
    is_resizable: Var[bool] = False
    is_draggable: Var[bool] = False
    resize_handles: Var[List[str]] = ["se"]

    _rename_props = {'dataGrid': 'data-grid'}


grid_layout = GridLayout.create
responsive_grid_layout = ResponsiveGridLayout.create
grid_layout_item = GridLayoutItem.create
