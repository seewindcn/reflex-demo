from typing import Any
import json
import reflex as rx
from . import antd

ex_columns = [
    dict(
        title='Id',
        dataIndex='key',
        key='key',
        sorter='true',
        defaultSortOrder='descend',
        render='(text) => <a>{text}</a>',
    ),
    dict(
        title='Name',
        dataIndex='name',
        key='name',
        sorter='true',
        render='',
    ),
    dict(
        title='Age',
        dataIndex='age',
        key='age',
    ),
    dict(
        title='Gender',
        dataIndex='gender',
        key='gender',
        filters=json.dumps([
            dict(text="Male", value="male"),
            dict(text="Female", value="female"),
        ]),
    ),
    dict(
        title='Address',
        dataIndex='address',
        key='address',
    ),
]


class AntdState(rx.State):
    """Define empty state to allow access to rx.State.router."""

    data_source: list[dict[str, Any]] = [
        dict(key='1', name='Mike', age=32, gender='male', address='11 Downing Street', ),
        dict(key='2', name='John', age=42, gender='female', address='12 Downing Street', ),
        dict(key='3', name='Jim', age=22, gender='male', address='13 Downing Street', ),
        dict(key='4', name='Expandable', age=52, gender='female', address='14 Downing Street', ),
        dict(key='5', name='Black', age=62, gender='male', address='15 Downing Street', ),
    ]

    columns = [
        dict(title='Id', dataIndex='key', key='key', ),
        dict(title='Name', dataIndex='name', key='name', ),
        dict(title='Age', dataIndex='age', key='age', ),
        dict(title='Address', dataIndex='address', key='address', ),
    ]

    def on_selection_change(self):
        print(self, 'works')
        rx.console_log('works')

    def on_table_change(self, pagination, filters, sorter):
        print("on_table_change:", pagination, filters, sorter)


def antd1() -> rx.Component:
    return rx.flex(
        antd.button("antd_demo ok"),
        rx.card(
            rx.text('antd_demo table'),
            antd.Table(
                data_source=AntdState.data_source, columns=AntdState.columns,
            )
        ),
        rx.card(
            rx.text('antd_demo tableEx'),
            antd.Table(
                id='antdEx1',
                data_source=AntdState.data_source, columns=ex_columns,
                filters={'gender': ['male']},
                on_change=AntdState.on_table_change,
            )
        ),
        antd.float_button(
            "floatButton", shape="circle",
            icon=antd.CustomerServiceOutlinedIcon(),
            right=50,
        ),
        direction="column",
    )


@rx.page('/antd_demo')
def index() -> rx.Component:
    return rx.center(
        rx.link('<- back', href='/'),
        rx.vstack(
            rx.heading("Dashboard", size="8"),
            rx.text("Welcome to Reflex!"),
            rx.text(
                "You can edit this page in ",
                rx.code("{your_app}/pages/dashboard.py"),
            ),
            antd1(),

            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )
