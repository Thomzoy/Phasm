print("Booting")

from time import sleep
import network
import socket

from configuration import COLORS, config, DEVICE

import helpers as h

h.reset_pins()

print("Testing LEDs")

pattern = DEVICE*[1023, 0]

for duty_cycle in pattern:
    h.set_rgb(**{color: duty_cycle for color in COLORS})
    sleep(0.2)

print("Testing WiFI")

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

ssids = [s[0] for s in sta_if.scan()]

if bytes(config["ssid"], "utf-8") in ssids:
    print(f"WiFi {config['ssid']} found, connecting...")

sta_if.connect(config["ssid"], config["wifi_pw"])

available_status = {
    network.STAT_IDLE: "IDLE",
    network.STAT_CONNECTING: "CONNECTING",
    network.STAT_WRONG_PASSWORD: "WRONG_PASSWORD",
    network.STAT_NO_AP_FOUND: "NO_AP_FOUND",
    network.STAT_GOT_IP: "CONNECTION_OK",
}

for trial in range(10):
    status = sta_if.status()
    string_status = available_status[status]
    print(f"Current status : {string_status}")
    if status == network.STAT_GOT_IP:
        break
    else:
        sleep(1)
"""
print("Testing Internet Connection")


def http_get(url):
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, "utf8"), end="")
        else:
            break


http_get("http://micropython.org/ks/test.html")

print("Tests Done !")
"""
