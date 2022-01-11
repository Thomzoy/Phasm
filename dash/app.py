# Run this app with `python app.py` and
# visit http://10.3.141.1:8000/ in your web browser.

import json
import pathlib
import os
from copy import deepcopy
from typing import Any, Dict, List, Union, Tuple

import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc

from tinydb import TinyDB, Query
from programs import all_programs, payload
from mqtt import get_client

device = dict(selected=False, color="dark")
devices = {i: device.copy() for i in [1, 2, 3, 4]}
db = TinyDB(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "db.json",
    )
)

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
    Input({"role": "ddm-button", "id": ALL}, "n_clicks"),
)
def activate_devices(n_clicks_list: List[int]) -> List[str]:
    """
    Callback to activate selected devices in the NavBar dropdown
    Will modify the global variable `devices`

    Parameters
    ----------
    n_clicks_list : List[int]
        List of `n_clicks` values
        First item corresponds to the "Select All" button
        Then `n_clicks_list[i]` corresponds to device n°i

    Returns
    -------
    List[str]
        List of colors to change the buttons' styles if a device is selected
    """

    global devices

    selects = [(n % 2 == 1) for n in n_clicks_list]

    if selects[0]:
        selects = len(selects) * [True]

    for i in devices:
        devices[i]["selected"] = selects[i]
        devices[i]["color"] = "success" if selects[i] else "dark"

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

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Load Parameters..."),
                    dbc.Select(
                        id="program-kwargs-select",
                        options=[
                            {"label": "Color Flash Params #1", "value": "color_cycle"},
                            {"label": "Color Flash Params #2", "value": "color_flash"},
                            {"label": "Storm Params #1", "value": "storm"},
                        ],
                    ),
                ]
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Save Parameters..."),
                    dbc.Input(
                        placeholder="Params name...", id="program-params-savename"
                    ),
                    dbc.Button("Save", id="program-params-save", n_clicks=0),
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

tabs = tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Program", tab_id="tab-1"),
                dbc.Tab(tab2_content, label="Parameters", tab_id="tab-2"),
                dbc.Tab(tab3_content, label="Send", tab_id="tab-3"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


@app.callback(
    Output("program-send", "color"),
    Input("program-send", "n_clicks"),
)
def send_program(n_clicks: int) -> str:
    """
    Publish the selected program + parameters to the MQTT topic

    Parameters
    ----------
    n_clicks : int
        clicks of the "Send" button

    Returns
    -------
    str
        color of the "Send" button
    """

    print(f"Sending {payload}")
    p = deepcopy(payload)

    if n_clicks is None:  # Handling callback call at startup
        return "primary"

    if n_clicks > 0:
        for id, kwarg in p["program_kwargs"].items():
            if "color" in id:
                # From HEX to RGB
                kwarg = tuple(int(kwarg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
                p["program_kwargs"][id] = kwarg

        client = get_client()
        for device_id, device in devices.items():
            if device["selected"]:
                client.publish(
                    f"esps/{device_id}", payload=json.dumps(p), qos=1, retain=False
                )
                print(f"Sent to device n°{device_id}")
        return "success"


@app.callback(
    Output("content", "children"),
    Output("program-kwargs-select", "options"),
    State("program-select", "value"),
    State({"role": "program_kwarg", "id": ALL}, "value"),
    State({"role": "program_kwarg", "id": ALL}, "id"),
    Input("program-kwargs-select", "value"),
    Input("tabs", "active_tab"),
)
def switch_tab(
    program: str,
    kwargs: List[Dict[str, Any]],
    ids: List[Dict[str, Any]],
    program_kwargs_name: str,
    at: str,
) -> Tuple[dbc.Card, List[Dict[str, Any]]]:
    """
    Callback to switch between tabs:
    - Tab 1 is to pick the program
    - Tab 2 is to pick the program's parameters
    - Tab 3 is to send the program
    This callback is also called when a saved program setting is picked

    Parameters
    ----------
    program : str
        name of the program, coming from the `program-select` Dropdown
    kwargs : List[Dict[str, Any]]
        kwargs of the program
    ids : List[Dict[str, Any]]
        List of elements ids, with 1 to 1 correspondance to the above kwargs
    program_kwargs_name : str
        Name of the selected program kwargs in Tab 2
    at : str
        Tab name

    Returns
    -------
    Union[None, dbc.Card]
        Content of the Tab
    """

    Q = Query()
    programs_kwargs = db.table("program_kwargs")
    program_kwargs_options = programs_kwargs.search(Q.program == program)
    program_kwargs_picked = (
        None
        if program_kwargs_name is None
        else programs_kwargs.get(Q.name == program_kwargs_name)
    )

    if program_kwargs_picked is not None:
        kwargs, ids = program_kwargs_picked["kwargs"], program_kwargs_picked["ids"]

    # Saving params
    global payload

    payload["program"] = program
    for kwarg, id_dict in zip(kwargs, ids):
        id = id_dict["id"]
        payload["program_kwargs"][id] = kwarg
    print(f"Payload: {payload}")

    if at in ["tab-1", "tab-3"]:
        # Those tabs already contains content
        return None, []
    elif at == "tab-2":
        return all_programs(program, payload), [
            {"label": p["name"], "value": p["name"]} for p in program_kwargs_options
        ]


@app.callback(
    Output("program-params-save", "color"),
    Output("program-params-savename", "placeholder"),
    Output("program-params-savename", "value"),
    State("program-select", "value"),
    State({"role": "program_kwarg", "id": ALL}, "value"),
    State({"role": "program_kwarg", "id": ALL}, "id"),
    State("program-params-savename", "value"),
    Input("program-params-save", "n_clicks"),
)
def save_params(
    program: str,
    kwargs: List[Dict[str, Any]],
    ids: List[Dict[str, Any]],
    save_name: str,
    save: int,
) -> Union[None, str]:

    if save < 1:
        return "primary", "Params name...", ""

    Q = Query()
    programs_kwargs = db.table("program_kwargs")

    if programs_kwargs.contains(Q.name == save_name):
        return "danger", f"Params with name {save_name} already exists", ""

    programs_kwargs.insert(
        dict(name=save_name, program=program, ids=ids, kwargs=kwargs)
    )

    return "success", f"Params saved with name {save_name}", ""


app.layout = html.Div([navbar, tabs])

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(port=8000, host="10.3.141.1", debug=True)
