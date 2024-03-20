import reflex as rx

from .datatable import index
from .antd_demo import index as antd_index  # noqa


app = rx.App()
app.add_page(index, route='/')
