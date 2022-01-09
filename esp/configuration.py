# config.py Local configuration for mqtt_as demo programs.
from mqtt_as import config

from machine import Pin, PWM

config["server"] = "10.3.141.1"  # Change to suit
config["port"] = 1883
# config['server'] = 'iot.eclipse.org'

# Not needed if you're only using ESP8266
config["ssid"] = "raspi-webgui"
config["wifi_pw"] = "ChangeMe"

# For demos ensure same calling convention for LED's on all platforms.
# ESP8266 Feather Huzzah reference board has active low LED's on pins 0 and 2.
# ESP32 is assumed to have user supplied active low LED's on same pins.
# Call with blue_led(True) to light


def ledfunc(pin):
    pin = pin

    def func(v):
        pin(not v)  # Active low on ESP8266

    return func


wifi_led = ledfunc(Pin(0, Pin.OUT, value=0))  # Red LED for WiFi fail/not ready yet
blue_led = ledfunc(Pin(2, Pin.OUT, value=1))  # Message received

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
