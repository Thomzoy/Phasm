print("Booting")

from machine import Pin, PWM
from time import sleep

from config import PORTS

COLORS = {color: PWM(Pin(pin)) for color, pin in PORTS.items()}

print("Testing LEDs")

pattern = [1023, 0, 1023, 0, 1023, 0]

for pwm in COLORS.values():
    for duty_cycle in pattern:
        pwm.duty(duty_cycle)
        sleep(0.5)
