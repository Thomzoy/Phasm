# config.py Local configuration for mqtt_as demo programs.
from mqtt_as import config

from machine import Pin, PWM, unique_id

import ubinascii

config["server"] = "10.3.141.1"
config["port"] = 1883

config["ssid"] = "Phasm"
config["wifi_pw"] = "HarryThePhasm"

PORTS = dict(
    R=13,
    G=32,
    B=27,
)

COLORS = {color: PWM(Pin(pin)) for color, pin in PORTS.items()}

PROGRAM = dict(
    current_program="color_cycle",
    program_kwargs={},
)

DEVICES = {
    "c8c9a3cbfe88": 1,
    "UNIQUE_ID_2": 2,
}

DEVICE = DEVICES[ubinascii.hexlify(unique_id()).decode("utf-8")]
