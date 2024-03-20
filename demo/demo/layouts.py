from typing import Callable
import reflex as rx


def layout1(path: str = ""):
    from .components.grid_layout import grid_layout, grid_layout_item

    def _layout(contents: Callable[[], rx.Component]):
        def _wrapper(*args, **kwargs) -> rx.Component:
            return grid_layout(
                # contents(*args, **kwargs),
                grid_layout_item(
                    key="header",
                    data_grid=dict(x=0, y=0, w=12, h=1, static=True),
                    class_name="border-2 border-gray-300",

                ),
                grid_layout_item(
                    key="navbar",
                    data_grid=dict(x=0, y=1, w=2, h=20, static=False),
                    class_name="border-2 border-gray-300",
                    is_resizable=True,
                ),
                grid_layout_item(
                    contents(*args, **kwargs),
                    key="body",
                    data_grid=dict(x=3, y=1, w=10, h=20, static=False),
                    class_name="border-2 border-gray-300",
                ),
                class_name="layout",
                cols=12,
                row_height=30,
                width=1200,
                auto_size=True,
            )
        return _wrapper

    return _layout


def layout2(path: str = ""):
    from .components.grid_layout import responsive_grid_layout, grid_layout_item

    def _layout(contents: Callable[[], rx.Component]):
        def _wrapper(*args, **kwargs) -> rx.Component:
            return responsive_grid_layout(
                # contents(*args, **kwargs),
                grid_layout_item(
                    key="header",
                    data_grid=dict(x=0, y=0, w=12, h=5, static=True),
                    class_name="border-2 border-gray-300",

                ),
                grid_layout_item(
                    key="navbar",
                    data_grid=dict(x=0, y=5, w=1, h=40, static=False),
                    class_name="border-2 border-gray-300",
                ),
                grid_layout_item(
                    contents(*args, **kwargs),
                    key="body",
                    data_grid=dict(x=1, y=1, w=11, h=20, static=False),
                    class_name="border-2 border-gray-300",
                ),
                class_name="layout",
                row_height=10,
                auto_size=True,
            )
        return _wrapper

    return _layout


default_layout = layout2

