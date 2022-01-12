import RPi.GPIO as GPIO
from gpiozero import CPUTemperature
import subprocess
import re


def get_signal_strength(signal: int):
    if signal >= -60:
        return "success"
    if signal >= -75:
        return "warning"
    if signal >= -85:
        return "danger"


def get_wlan_infos():
    connected = (
        subprocess.run(
            ["iw", "dev", "wlan1", "station", "dump"],
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .split("Station ")[1:]
    )

    with open("/var/lib/misc/dnsmasq.leases", "r") as f:
        leases = f.read()

    mac_addresses = [s.split(" ")[0] for s in connected]
    signals = [int(re.search(r"(.\d+) dBm", s).groups()[0]) for s in connected]
    signals_strengh = [get_signal_strength(s) for s in signals]
    names = [
        re.search(f"{mac}\s[\d.]*\s(.*?)\s", leases).groups()[0]
        for mac in mac_addresses
    ]

    connected_infos = [
        {"MAC Adress": m, "Signal": s, "Signal Strengh": ss, "Name": n}
        for (m, s, ss, n) in zip(mac_addresses, signals, signals_strengh, names)
    ]

    connected_infos.sort(key=lambda el: el["Signal"], reverse=True)

    return connected_infos


def get_cpu_temp():
    """
    Get the CPU temperature
    Returns it, along with a category.
    """
    temp = round(CPUTemperature().temperature, 1)

    if temp <= 60:
        return temp, "success"
    if temp <= 75:
        return temp, "warning"
    return temp, "danger"
