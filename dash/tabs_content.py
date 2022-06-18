import dash_daq as daq
from dash import html
import dash_bootstrap_components as dbc

import system_infos

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Select Program", className="card-text"),
            dbc.Select(
                id=dict(role="program", id="program_name"),
                options=[
                    {"label": "Color Cycle", "value": "color_cycle"},
                    {"label": "Color Flash", "value": "color_flash"},
                    {"label": "Storm", "value": "storm"},
                    {"label": "Ping Pong", "value": "ping_pong"},
                    {"label": "Change Program", "value": "overwrite"}
                ],
            ),
            html.P("", className="card-text"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Load Params..."),
                    dbc.Select(
                        id="program-kwargs-select",
                        options=[],
                    ),
                ]
            ),
            dbc.InputGroup(
                [
                    dbc.Button("Save Params...", id="program-params-save", n_clicks=0),
                    dbc.Input(
                        placeholder="Params name...", id="program-params-savename"
                    ),
                ]
            ),
        ]
    )
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Send to ESPs", className="card-text"),
            dbc.Button(
                "Go !",
                id="program-send",
                color="primary",
            ),
            html.P("", className="card-text"),
        ]
    ),
    className="mt-3",
)


def get_tab4_content(wlan_infos):
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Div(
                        [
                            html.H5(
                                f"Connected device : {device['Name']}",
                                className="mb-1",
                            ),
                            html.Small(
                                device["Signal"],
                                className=f"text-{device['Signal Strengh']}",
                            ),
                        ],
                        className="d-flex w-100 justify-content-between",
                    ),
                    html.P(f"MAC Adress: {device['MAC Adress']}", className="mb-1"),
                ]
            )
            for device in wlan_infos
        ]
    )
