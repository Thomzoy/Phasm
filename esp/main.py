from machine import Pin, PWM
import time

from boot import COLORS

while True:
    for color, pwm in COLORS.items():
        print(f"Color : {color}")
        for t in range(512):
            pwm.duty(t)
            time.sleep(0.01)
        pwm.duty(0)
