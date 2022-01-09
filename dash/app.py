# Run this app with `python app.py` and
# visit http://10.3.141.1:8000/ in your web browser.

import json

from copy import deepcopy

import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc

from programs import all_programs, payload

from mqtt import get_client

device = dict(selected=False, color="dark")
devices = {i: device.copy() for i in [1, 2, 3, 4]}

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
        }
    ],
)

##### NAVBAR #####

ddm = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(
            dbc.Badge(
                f"Select All",
                pill=True,
                color="primary",
                className="me-1",
                id={"id": 0, "role": "ddm-badge"},
            ),
            id={"id": 0, "role": "ddm-button"},
            n_clicks=0,
            toggle=False,
        ),
        dbc.DropdownMenuItem(divider=True),
    ]
    + [
        dbc.DropdownMenuItem(
            dbc.Badge(
                f"ESP #{i}",
                pill=True,
                color=params["color"],
                className="me-1",
                id={"id": i, "role": "ddm-badge"},
            ),
            id={"id": i, "role": "ddm-button"},
            n_clicks=0,
            toggle=False,
        )
        for i, params in devices.items()
    ],
    nav=True,
    in_navbar=True,
    label="Select device",
)


@app.callback(
    Output({"role": "ddm-badge", "id": ALL}, "color"),
    [Input({"role": "ddm-button", "id": ALL}, "n_clicks")],
)
def activate_devices(n_clicks_list):

    global devices

    selects = [(n % 2 == 1) for n in n_clicks_list]

    if selects[0]:
        selects = len(selects) * [True]

    for i in devices:
        devices[i]["selected"] = selects[i]
        devices[i]["color"] = "success" if selects[i] else "dark"
    print(devices)
    return ["success" if selects[0] else "dark"] + [
        d["color"] for d in devices.values()
    ]


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        ddm,
    ],
    brand="Phasm - Sceno",
    brand_href="#",
    color="primary",
    dark=True,
)

##### TABS #####

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Select Program", className="card-text"),
            dbc.Select(
                id="program-select",
                options=[
                    {"label": "Color Cycle", "value": "color_cycle"},
                    {"label": "Color Flash", "value": "color_flash"},
                    {"label": "Storm", "value": "storm"},
                ],
            ),
            html.P("", className="card-text"),
        ]
    ),
    className="mt-3",
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

tabs = tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Program", tab_id="tab-1"),
                dbc.Tab(label="Parameters", tab_id="tab-2"),
                dbc.Tab(tab3_content, label="Send", tab_id="tab-3"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


@app.callback(Output("program-send", "color"), Input("program-send", "n_clicks"))
def send_program(n_clicks):

    print(f"Sending {payload}")
    p = deepcopy(payload)

    if n_clicks is None:
        return "primary"

    if n_clicks > 0:
        for id, kwarg in p["program_kwargs"].items():
            if "color" in id:
                # From HEX to RGB
                kwarg = tuple(int(kwarg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
                p["program_kwargs"][id] = kwarg

        client = get_client()
        client.publish("tpj_test_topic", payload=json.dumps(p), qos=1, retain=False)
        print("Sent ")
        return "success"


@app.callback(
    Output("content", "children"),
    State("program-select", "value"),
    State({"role": "program_kwarg", "id": ALL}, "value"),
    State({"role": "program_kwarg", "id": ALL}, "id"),
    Input("tabs", "active_tab"),
)
def switch_tab(program, kwargs, ids, at):

    # Saving params
    global payload

    payload["program"] = program
    for kwarg, id_dict in zip(kwargs, ids):
        id = id_dict["id"]
        payload["program_kwargs"][id] = kwarg
    print(f"Payload: {payload}")
    
    if at in ["tab-1", "tab-3"]:
        return None
    elif at == "tab-2":
        return all_programs(program, payload)


app.layout = html.Div([navbar, tabs])

if __name__ == "__main__":
    app.run_server(port=8000, host="10.3.141.1", debug=True)
