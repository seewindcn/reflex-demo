from __future__ import annotations

from typing import Any, Dict, List, Union, Type
import uuid

import reflex as rx
from reflex.components.gridjs.datatable import DataTable
from reflex.components.component import Component
from reflex.components.tags import Tag
from reflex.utils import imports, types
from reflex.utils.serializers import serialize
from reflex.vars import BaseVar, ComputedVar, Var


def ui_name(cell: rx.Var, row: rx.Var, state: Type[rx.State]) -> rx.Component:
    href_var = Var.create_safe(cell._var_full_name, _var_is_local=False, _var_is_string=False)
    return rx.link(cell, href=href_var)


def ui_code(cell: rx.Var, row: rx.Var, state: Type[rx.State]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(cell, variant="soft"),
        ),
        rx.popover.content(
            rx.flex(
                rx.avatar(
                    "2",
                    fallback="RX",
                    radius="full"
                ),
                rx.box(
                    rx.text_area(placeholder="Write a comment…", style={"height": 80}),
                    rx.flex(
                        rx.checkbox("Send to group"),
                        rx.popover.close(
                            rx.button(cell, size="1", on_click=lambda: state.click(cell, row))
                        ),
                        spacing="3",
                        margin_top="12px",
                        justify="between",
                    ),
                    flex_grow="1",
                ),
                spacing="3"
            ),
            style={"width": 360},
        )
    )



def ui_url(cell: rx.Var, row: rx.Var, state: Type[rx.State]) -> rx.Component:
    return rx.link(cell, on_click=lambda: state.click(cell, row))


class DataTableEx(DataTable):
    """A data table component."""

    alias = "DataTableExGrid"
    
    # _state: Type[rx.State] = None

    @classmethod
    def create(cls, *children, **props):
        _state = props.pop('_state')
        rs = super().create(cls, *children, **props)
        if rs.id is None:
            rs.id = uuid.uuid4().hex
        # rs._state = _state
        return rs

    def _get_unique_name(self) -> str:
        return f'GridjsEx_{self.id}'

    def _get_columns_name(self) -> str:
        return f'{self._get_unique_name()}_columns'

    def _get_ex_params(self):
        from .datatable import State
        cell_var = Var.create_safe('{cell}')
        row_var = Var.create_safe('{row}')
        return cell_var, row_var, State  # self._state

    def _get_custom_code(self) -> str | None:
        cell_var, row_var, state = self._get_ex_params()
        return f"""
        function {self._get_columns_name()} () {{
            const [addEvents, connectError] = useContext(EventLoopContext);
            return [{{
                    name: "FirstName",
                    formatter: (cell, row) => {{
                        return _({ui_name(cell_var, row_var, state)});
                    }},
                }},  "LastName", 
                {{
                    name: "Code",
                    formatter: (cell, row) => {{
                        return _({ui_code(cell_var, row_var, state)});
                    }},
                }}, 
                {{
                    name: "Url",
                    formatter: (cell, row) => {{
                        return _({ui_url(cell_var, row_var, state)});
                    }},
                }},
            ]
        }}
        """

    def _get_imports(self) -> imports.ImportDict:
        cell_var, row_var, state = self._get_ex_params()
        uis = [op(cell_var, row_var, state) for op in [ui_code, ui_name, ui_url]]
        return imports.merge_imports(
            super()._get_imports(),
            {self.library: {imports.ImportVar(tag='_'), imports.ImportVar(tag='h')}},
            {"": {imports.ImportVar(tag="gridjs/dist/theme/mermaid.css")}},
            *[ui.get_imports() for ui in uis],
        )

    def _render(self) -> Tag:
        if isinstance(self.data, Var) and types.is_dataframe(self.data._var_type):
            self.columns = BaseVar(
                _var_name=f"{self.data._var_name}.columns",
                _var_type=List[Any],
                _var_full_name_needs_state_prefix=True,
            )._replace(merge_var_data=self.data._var_data)
            self.data = BaseVar(
                _var_name=f"{self.data._var_name}.data",
                _var_type=List[List[Any]],
                _var_full_name_needs_state_prefix=True,
            )._replace(merge_var_data=self.data._var_data)
        if types.is_dataframe(type(self.data)):
            # If given a pandas df break up the data and columns
            data = serialize(self.data)
            assert isinstance(data, dict), "Serialized dataframe should be a dict."
            self.columns = Var.create_safe(data["columns"])
            self.data = Var.create_safe(data["data"])

        tag = (
            super()
            ._render()
            .remove_props("columns", )
        )
        tag.special_props.add(
            Var.create_safe(
                f"columns={{{self._get_columns_name()}()}}",
                _var_is_local=True,
                _var_is_string=False,
            ),
        )
        # Render the table.
        return tag



