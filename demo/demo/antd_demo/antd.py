from typing import List, Any, Union, Dict, Optional
from functools import lru_cache
import json

import reflex as rx

from reflex.constants import EventTriggers
from reflex import Component, Var
from reflex.components.tags import Tag
from reflex.utils import imports

"""
. import type support: 
    import type { DocumentContext } from 'next/document';
    import type { ColumnsType } from 'antd/es/table';
. 
"""

# rx.chakra.select


class AntdComponent(Component):
    """A component that wraps a Chakra component."""

    library = "antd"

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
        return {
            (160, "AntdProvider"): antd_provider,
        }

    # @classmethod
    # @lru_cache(maxsize=None)
    # def _get_dependencies_imports(cls) -> imports.ImportDict:
    #     """Get the imports from lib_dependencies for installing.
    #
    #     Returns:
    #         The dependencies imports of the component.
    #     """
    #     return {
    #         dep: [imports.ImportVar(tag=None, render=False)]
    #         for dep in [
    #             "@chakra-ui/system@2.5.7",
    #             "framer-motion@10.16.4",
    #         ]
    #     }


class AntdProvider(AntdComponent):
    """Top level Chakra provider must be included in any app using chakra components."""

    tag = "ConfigProvider"
    alias = "AntdConfigProvider"

    theme: Var[str]

    @classmethod
    def create(cls) -> Component:
        """Create a new ChakraProvider component.

        Returns:
            A new ChakraProvider component.
        """
        return super().create(
            theme=Var.create("theme", _var_is_local=False),
        )

    def _get_imports(self) -> imports.ImportDict:
        _imports = super()._get_imports()
        _imports.setdefault("/utils/theme.js", []).append(
            imports.ImportVar(tag="theme", is_default=True),
        )
        return _imports

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
        return {
            (170, "AntdRegistryProvider"): antd_registry_provider,
        }


antd_provider = AntdProvider.create()


class AntdRegistryProvider(Component):
    library = "@ant-design/nextjs-registry"
    tag = "AntdRegistry"


antd_registry_provider = AntdRegistryProvider.create()

# class ChakraColorModeProvider(Component):
#     """Next-themes integration for chakra colorModeProvider."""
#
#     library = "/components/reflex/chakra_color_mode_provider.js"
#     tag = "ChakraColorModeProvider"
#     is_default = True
#
#
# chakra_color_mode_provider = ChakraColorModeProvider.create()


class IconComponent(Component):
    library = "@ant-design/icons"


class CustomerServiceOutlinedIcon(IconComponent):
    tag = 'CustomerServiceOutlined'


class ButtonComponent(AntdComponent):
    tag = "Button"


class FloatButton(AntdComponent):
    tag = "FloatButton"

    shape: Var[str]
    icon: Var[IconComponent]
    type: Var[str] = 'primary'

    def _get_imports(self) -> imports.ImportDict:
        return imports.merge_imports(
            super()._get_imports(),
            self.icon._var_type().get_imports(),
            # {"@ant-design/icons": {imports.ImportVar(tag="CustomerServiceOutlined")}},
        )


class Table(AntdComponent):
    tag = 'Table'

    data_source: rx.Var[list[dict[str, Any]]]
    columns: rx.Var[list[dict[str, Any]]]
    filters: Optional[rx.Var[dict[str, Any]]]
    # columns: Union[rx.Var[list[dict[str, Any]]], list[dict[str, Any]]]
    # rowSelection: rx.Var[dict[str, Any]]

    @property
    def is_ex_columns(self) -> bool:
        return not bool(self.columns._var_data)

    def _get_imports(self) -> imports.ImportDict:
        _imports = super()._get_imports()
        # _imports.setdefault(self.__fields__["library"].default, []).append(
        #     imports.ImportVar(tag="TableColumnsType", is_default=False),
        # )
        return _imports

    def get_event_triggers(self) -> Dict[str, Any]:
        _triggers = super().get_event_triggers()
        _triggers.update({
            EventTriggers.ON_CHANGE: lambda pagination, filters, sorter: [pagination, filters, sorter],
        })
        return _triggers

    def _get_unique_name(self) -> str:
        return f'AntdTable_{self.id}'

    def _get_columns_name(self) -> str:
        return f'{self._get_unique_name()}_columns'

    def _get_columns_code(self) -> str:
        cell_var = Var.create_safe('{text}')
        def _columns() -> str:
            columns = ['[']
            cols = json.loads(self.columns._var_name_unwrapped)
            for col in cols:
                columns.append('{')
                for k, v in col.items():
                    if k not in ['render', 'filters', 'sorter']:
                        columns.append(f"  {k}: '{v}',")
                    else:
                        if col['key'] == 'name' and k == 'render':
                            columns.append(f"  {k}: (text) => {rx.code(cell_var)},")
                        else:
                            columns.append(f"  {k}: {v},")
                columns.append('},')
            columns.append('];')
            return '\n'.join(columns)
        return f"""
        function {self._get_columns_name()} () {{
            const [addEvents, connectError] = useContext(EventLoopContext);
            return {_columns()}
        }}
        """

    def _get_custom_code(self) -> str | None:
        if not self.is_ex_columns:
            return

        codes = [
            self._get_columns_code(),
        ]
        return '\n'.join(codes)

    def _render(self, props: dict[str, Any] | None = None) -> Tag:
        if not self.is_ex_columns:
            return super()._render(props=props)
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


icon = IconComponent.create
button = ButtonComponent.create
float_button = FloatButton.create
table = Table.create







