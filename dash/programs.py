import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc

all_programs = dict(
    color_cycle = dbc.Card(
        dbc.CardBody(
            [
                html.P("Color Cycle!", className="card-text"),
                dbc.Button("Don't click here", color="danger"),
            ]
        ),
        className="mt-3",
    ),
    color_flash = dbc.Card(
        dbc.CardBody(
            [
                html.P("Color Flash!", className="card-text"),
                dbc.Button("Don't click here", color="danger"),
            ]
        ),
        className="mt-3",
    ),
    storm = dbc.Card(
        dbc.CardBody(
            [
                html.P("Storm!", className="card-text"),
                dbc.Button("Don't click here", color="danger"),
            ]
        ),
        className="mt-3",
    ),
    default = dbc.Card(
        dbc.CardBody(
            [
                html.P("No program selected", className="card-text"),
            ]
        ),
        className="mt-3",
    )
)