# Run this app with `python app.py` and
# visit http://10.3.141.1:8000/ in your web browser.

# This runs a persistent app that also hosts the Flask server that is then accessed through mqtt
# With this refactoring, the app is just seen as a way to send up-level parameters to the main process,
#   that in turn pushes them to the esps.

import json
import pathlib
import os
from copy import deepcopy
from typing import Any, Dict, List, Union, Tuple
from time import time

import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html, dcc
import dash_bootstrap_components as dbc

from tinydb import TinyDB, Query
from programs import all_programs, get_clear_payload

import tabs_content
import system_infos

from dash_mqtt import get_client

device = dict(selected=False, color="dark", type="ESP")
devices = {i: device.copy() for i in [1, 2, 3, 4, 5, 6]}
devices[6]["type"] = "MASTER"

db = TinyDB(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "db.json",
    ),
    indent=4,
    separators=(",", ": "),
)

payload = get_clear_payload()

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

# Uncomment to recover Temperature... I think it's pretty useless and fails outside raspberry
# temperature_badge = dbc.Badge(
#     "",
#     pill=True,
#     color="primary",
#     id="temperature_badge",
#     class_name="button",
# )
# @app.callback(
#     Output("temperature_badge", "children"),
#     Output("temperature_badge", "color"),
#     Input("temperature_badge", "n_clicks"),
# )
# def display_cpu_temp(n_clicks: int) -> str:
#     T, color = system_infos.get_cpu_temp()
#     return f"CPU : {T}°", color


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
                f"{params['type']} #{i}",
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
    prevent_initial_call=True,
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
        # dbc.NavItem(
        #     temperature_badge,
        #     class_name="d-inline-flex align-items-center justify-content-start",
        # ),
        ddm,
    ],
    brand="Phasm - Sceno",
    brand_href="#",
    color="primary",
    dark=True,
)

##### TABS #####

tabs = tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(tabs_content.tab1_content, label="Program", tab_id="tab-1"),
                dbc.Tab(tabs_content.tab2_content, label="Parameters", tab_id="tab-2"),
                dbc.Tab(tabs_content.tab3_content, label="Send", tab_id="tab-3"),
                dbc.Tab(label="System", tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


#### CALLBACKS ####

@app.callback(
    Output("program-send", "color"),
    Input("program-send", "n_clicks"),
    prevent_initial_call=True,
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
    global HOST, MQTT_PORT
    p = deepcopy(payload)
    print("picked_payload: ",payload)
    if n_clicks > 0:
        for id, kwarg in p["program_kwargs"].items():
            if "color" in id:
                # From HEX to RGB
                kwarg = tuple(int(kwarg.lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))
                p["program_kwargs"][id] = kwarg

        client = get_client(host_address=HOST, port=MQTT_PORT)

        payload_json = json.dumps(p)
        for device_id, device in devices.items():
            topic = f"esps/{device_id}" if device["type"] == "ESP" else "dash/main"
            if device["selected"]:
                target=""
                if payload["program"] == "overwrite":
                    target = "/overwrite"
                client.publish(
                    f"{topic}{target}", payload=json.dumps(p), qos=1, retain=False
                )
                print(f"Sent to device n°{device_id} on topic {topic}")
                print("payload: ", payload)
        return "success"


@app.callback(
    Output("fake-placeholder", "children"),
    Input({"role": "program", "id": "program_name"}, "value"),
    Input({"role": "program_kwarg", "id": ALL}, "value"),
    Input({"role": "program_kwarg", "id": ALL}, "id"),
    prevent_initial_call=True,
)
def save_single_param(p: str, vals: List[Any], ids: List[Any]):
    """
    Save a parameter when its value is changed
    """
    global payload

    trig = dash.callback_context.triggered[0]
    if trig["value"] is None:
        return ""

    v = trig["value"]
    keys = json.loads(trig["prop_id"][:-6])

    if keys["role"] == "program":
        payload = get_clear_payload()
        payload["program"] = v
        return ""

    if keys["role"] == "program_kwarg":
        payload["program_kwargs"][keys["id"]] = v
        return ""


@app.callback(
    Output("content", "children"),
    Output("program-kwargs-select", "options"),
    Input("program-kwargs-select", "value"),
    Input("tabs", "active_tab"),
)
def switch_tab(
        program_kwargs_name: str,
        at: str,
        prevent_initial_callback=True,
) -> Tuple[dbc.Card, List[Dict[str, Any]]]:
    """
    Callback to switch between tabs:
    - Tab 1 is to pick the program
    - Tab 2 is to pick the program's parameters
    - Tab 3 is to send the program
    This callback is also called when a saved program setting is picked

    Parameters
    ----------
    program_kwargs_name : str
        Name of the selected program kwargs in Tab 2
    at : str
        Tab name

    Returns
    -------
    Union[None, dbc.Card]
        Content of the Tab
    """

    global payload

    trigger_id = dash.callback_context.triggered[0]["prop_id"]
    program = payload["program"]

    Q = Query()
    programs_kwargs = db.table("program_kwargs")
    program_kwargs_options = programs_kwargs.search(Q.program == program)

    program_kwargs_picked = (
        dict()
        if (
                (program_kwargs_name is None) or ("program-kwargs-select" not in trigger_id)
        )
        else programs_kwargs.get(Q.name == program_kwargs_name)
    )
    for k, v in program_kwargs_picked.get("program_kwargs", dict()).items():
        payload["program_kwargs"][k] = v

    if at in ["tab-1", "tab-3"]:
        # Those tabs already contains content
        return None, []
    elif at == "tab-2":
        return all_programs(program, payload), [
            {"label": p["name"], "value": p["name"]} for p in program_kwargs_options
        ]
    elif at == "tab-4":
        wlan_infos = system_infos.get_wlan_infos()
        return tabs_content.get_tab4_content(wlan_infos), []


@app.callback(
    Output("program-params-save", "color"),
    Output("program-params-savename", "placeholder"),
    Output("program-params-savename", "value"),
    State("program-params-savename", "value"),
    Input("program-params-save", "n_clicks"),
    prevent_initial_call=True,
)
def save_params(
        save_name: str,
        save: int,
) -> Union[None, str]:
    global payload

    if save < 1:
        return "primary", "Params name...", ""

    Q = Query()
    programs_kwargs = db.table("program_kwargs")

    if programs_kwargs.contains(Q.name == save_name):
        return "danger", f"Params with name {save_name} already exists", ""

    if not save_name:
        return "danger", f"Please type a name", ""

    programs_kwargs.insert(
        dict(
            name=save_name,
            program=payload["program"],
            program_kwargs=payload["program_kwargs"],
        )
    )

    return "success", f"Params saved with name {save_name}", ""


placeholder = html.P("", id="fake-placeholder")

# fade_callback(app)

app.layout = html.Div([navbar, tabs, placeholder])

if __name__ == "__main__":
    # My PC
    #HOST = "127.0.0.1"
    #PORT = 1883

     # Pi
    HOST = "10.3.141.1"
    DASH_PORT = 8000
    MQTT_PORT = 1883
    app.run_server(host=HOST, port=DASH_PORT, debug=True)
