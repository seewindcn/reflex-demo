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
                    data_grid=dict(x=0, y=0, w=12, h=1, static="true"),
                ),
                grid_layout_item(
                    key="navbar",
                    data_grid=dict(x=0, y=1, w=2, h=20, static="true"),
                ),
                grid_layout_item(
                    contents(*args, **kwargs),
                    key="body",
                    data_grid=dict(x=3, y=2, w=10, h=20, static="true"),
                ),
                class_name="layout",
                cols=12,
                rowHeight=30,
                width=1200,
                auto_size=True,
            )
        return _wrapper

    return _layout


default_layout = layout1
