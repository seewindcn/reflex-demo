"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from typing import List

from rxconfig import config

import reflex as rx

from .components import DataTableEx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

    data: List = [
        ["Lionel", "Messi", "PSG", "/abc"],
        ["Christiano", "Ronaldo", "Al-Nasir", "/def"]
     ]
    columns: List[str] = ["First Name", "Last Name", "Code", "Url"]

    def click(self, cell, row):
        print('click', cell, row)


def index() -> rx.Component:
    return rx.center(
        # rx.theme_panel(),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text("Get started by editing ", rx.code(filename)),
            rx.button(
                "Check out our docs!",
                on_click=lambda: rx.redirect(docs_url),
                size="4",
            ),
            DataTableEx(
                # _state=State,
                data=State.data,
                columns=State.columns,
            ),

            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )


app = rx.App()
app.add_page(index)
