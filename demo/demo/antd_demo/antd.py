from typing import List, Any, Union, Dict, Optional
from types import LambdaType
from functools import lru_cache
import json

from pydantic import PrivateAttr
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
    _expandable: Optional[dict] = PrivateAttr(default=None)
    # columns: Union[rx.Var[list[dict[str, Any]]], list[dict[str, Any]]]
    # rowSelection: rx.Var[dict[str, Any]]

    @property
    def is_ex_columns(self) -> bool:
        return self.columns is not None and not bool(self.columns._var_data)

    @property
    def is_ex_expandable(self) -> bool:
        return self._expandable is not None

    @property
    def is_ex(self) -> bool:
        return self.is_ex_columns or self.is_ex_expandable

    def __init__(self, *args, _expandable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._expandable = _expandable

    def _get_imports(self) -> imports.ImportDict:
        import_list = []
        _imports = super()._get_imports()

        def _check_obj(d: Any):
            if isinstance(d, dict):
                for k, v in d.items():
                    _check_obj(v)
            elif isinstance(d, list):
                for i in d:
                    _check_obj(i)
            elif isinstance(d, rx.Component):
                import_list.append(d.get_imports())
            elif callable(d):
                _check_obj(d())
        for ex in [self._expandable, ]:
            _check_obj(ex)
        # _imports.setdefault(self.__fields__["library"].default, []).append(
        #     imports.ImportVar(tag="TableColumnsType", is_default=False),
        # )
        if import_list:
            return imports.merge_imports(_imports, *import_list)
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

    def _get_expandable_name(self) -> str:
        return f'{self._get_unique_name()}_expandable'

    @staticmethod
    def _get_ex_code(name: str, code_name: str, items: Union[dict, list]) -> str:
        cell_var = Var.create_safe('{text}')

        def _kvs(_items: dict, lines=None, sep=''):
            lines.append('{')
            for k, v in _items.items():
                if k not in [
                    'render', 'filters', 'sorter',
                    'expandedRowRender', 'rowExpandable',
                ]:
                    lines.append(f"  {k}: '{v}',")
                else:
                    if isinstance(v, LambdaType):
                        lines.append(f"  {k}: (record) => {v(None)},")
                    else:
                        lines.append(f"  {k}: {v},")
            lines.append(f'}}{sep}')

        def _columns() -> str:
            columns = ['[']
            for col in items:
                _kvs(col, columns, sep=',')
            columns.append('];')
            return '\n'.join(columns)

        def _dict() -> str:
            lines = []
            _kvs(items, lines, sep=';')
            return '\n'.join(lines)

        return f"""
        function {code_name} () {{
            const [addEvents, connectError] = useContext(EventLoopContext);
            return {_columns() if isinstance(items, list) else _dict()}
        }}
        """

    def _get_columns_code(self) -> str:
        cols = json.loads(self.columns._var_name_unwrapped)
        return self._get_ex_code('columns', self._get_columns_name(), cols)

    def _get_expandable_code(self) -> str:
        return self._get_ex_code('expandable', self._get_expandable_name(), self._expandable)

    def _get_custom_code(self) -> str | None:
        if not self.is_ex:
            return

        codes = [
            self._get_columns_code() if self.is_ex_columns else "",
            self._get_expandable_code() if self.is_ex_expandable else "",
        ]
        return '\n'.join(codes)

    def _render(self, props: dict[str, Any] | None = None) -> Tag:
        if not self.is_ex:
            return super()._render(props=props)
        tag = (
            super()
            ._render()
            .remove_props("columns", )
        )
        if self.is_ex_columns:
            tag.special_props.add(
                Var.create_safe(f"columns={{{self._get_columns_name()}()}}"),
            )
        if self.is_ex_expandable:
            tag.special_props.add(
                Var.create_safe(f"expandable={{{self._get_expandable_name()}()}}"),
            )
        # Render the table.
        return tag


icon = IconComponent.create
button = ButtonComponent.create
float_button = FloatButton.create
table = Table.create







