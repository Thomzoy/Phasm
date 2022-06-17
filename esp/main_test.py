from machine import Pin, PWM, unique_id
from time import sleep

PINS = [22,5,0]

PWMS = []
for pin in PINS:
    PWMS.append(PWM(Pin(pin)))

while True:
    for p in PWMS:
        p.duty(0)
    for p in PWMS:
        p.duty(1023)
        sleep(1)
        p.duty(0)