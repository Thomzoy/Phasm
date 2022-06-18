import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

# This is the html binding for programs, careful, names must match to send the right payload.

def get_clear_payload():
    return dict(program=None, program_kwargs=dict())


def all_programs(program, payload):

    if program == "color_cycle":
        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Color Cycle!", className="card-text"),
                ]
            ),
            className="mt-3",
        )

    if program == "color_flash":
        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Color Flash!", className="card-text"),
                    html.Div(
                        [
                            dbc.Label("Select a color"),
                            dbc.Input(
                                value=payload["program_kwargs"].get(
                                    "flash_color", "#000000"
                                ),
                                type="color",
                                id=dict(role="program_kwarg", id="flash_color"),
                                style={"width": 75, "height": 50},
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-3",
        )

    if program == "ping_pong":

        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Ping Pong!", className="card-text"),
                    html.Div(
                        [
                            dbc.Label("Select a color"),
                            dbc.Input(
                                value=payload["program_kwargs"].get(
                                    "color_fade", "#000000"
                                ),
                                type="color",
                                id=dict(role="program_kwarg", id="color_fade"),
                                style={"width": 75, "height": 50},
                            ),
                            dbc.Label("Select a fade duration"),
                            dcc.Input(
                                type="number",
                                value=payload["program_kwargs"].get("duration_fade",1),
                                id=dict(role="program_kwarg", id="duration_fade"),
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-3",
        )

    if program == "color_cycle":

        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Color Cycle", className="card-text"),
                    html.Div(
                        [
                            dbc.Label("Select a duration"),
                            dcc.Input(
                                type="number",
                                value=payload["program_kwargs"].get("duration_cycle",1),
                                id=dict(role="program_kwarg", id="duration_cycle"),
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-3",
        )

    if program == "storm":
        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Storm!", className="card-text"),
                    html.Div(
                        [
                            dbc.Label("Select a color", id="color"),
                            dbc.Input(
                                value=payload["program_kwargs"].get(
                                    "storm_color", "#000000"
                                ),
                                type="color",
                                id=dict(role="program_kwarg", id="storm_color"),
                                style={"width": 75, "height": 50},
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.P("Duration (s)"),
                            dbc.Input(
                                value=payload["program_kwargs"].get("storm_period", 10),
                                type="number",
                                min=10,
                                max=60,
                                step=1,
                                id=dict(
                                    role="program_kwarg",
                                    id="storm_period",
                                ),
                            ),
                        ],
                        id="styled-numeric-input",
                    ),
                ]
            ),
            className="mt-3",
        )

    if (program == "default") or program is None:
        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("No program selected", className="card-text"),
                ]
            ),
            className="mt-3",
        )

    if program == "overwrite":
        selected_program = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Overwrite", className="card-text"),
                    html.Div(
                        [
                            dbc.Label("Paste new programm code here", id="code"),
                            dbc.Textarea(
                                value="",
                                size="lg",
                                id=dict(role="program_kwarg", id="program_code"),
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-3",
        )

    return selected_program

