# config.py Local configuration for mqtt_as demo programs.
from mqtt_as import config

from machine import Pin, PWM, unique_id

import ubinascii

config["server"] = "10.3.141.1"
config["port"] = 1883

config["ssid"] = "Phasm"
config["wifi_pw"] = "HarryThePhasm"

PORTS = dict(
    R=5,
    G=0,
    B=22,
)

COLORS = {color: PWM(Pin(pin)) for color, pin in PORTS.items()}

PROGRAM = dict(
    current_program="storm",
    program_kwargs={},
)

DEVICES = {
    "78e36d1a7864": 1,
    "78e36d1a7ed8": 2,
    "78e36d1a7e38": 3,
    "78e36d1a85c8": 4,
    "78e36d1a6ab0": 5,
}

DEVICE = DEVICES[ubinascii.hexlify(unique_id()).decode("utf-8")]

from machine import unique_id
import ubinascii
print(ubinascii.hexlify(unique_id()).decode("utf-8"))