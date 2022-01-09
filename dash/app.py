# Run this app with `python app.py` and
# visit http://10.3.141.1:8000/ in your web browser.

import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc

import mqtt

import json

from programs import all_programs

device = dict(selected=False, color="dark")

devices = {i: device.copy() for i in [1, 2, 3, 4]}

client = mqtt.client
#client.loop_forever()

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
        }
    ],
    # external_stylesheets=[dbc.themes.DARKLY],
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
                dbc.Tab(tab3_content, label="Send", tab_id="tab-3")
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

@app.callback(Output("content", "children"), [State("program-select", "value"), Input("tabs", "active_tab")])
def switch_tab(program, at):
    if at in["tab-1","tab-3"]:
        return None
    elif at == "tab-2":
        if program in all_programs:
            return all_programs[program]
        else:
            return all_programs['default']

app.layout = html.Div(
    [
        navbar,
        tabs
    ]
)

def update_output(n_clicks, color):

    rgb_color = [(c + 1) * 4 - 1 for c in color["rgb"].values()][
        :-1
    ]  # Remove the alpha parameter

    payload = dict(
        program="color_flash",
        program_kwargs={"color": rgb_color},
    )

    payload = json.dumps(payload)

    client.publish("tpj_test_topic", payload=payload, qos=1, retain=False)

    return "Clicks: {}. The selected color is {}.".format(n_clicks, color)


if __name__ == "__main__":
    app.run_server(port=8000, host="10.3.141.1", debug=True)
