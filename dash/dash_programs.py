import json
import time
import asyncio
import random


# This is meant to be used by the main in dash.

async def broadcast_name_and_kwargs(client, payload):
    """
    """
    for device_id in range(1, 6):
        client.publish(f"esps/{device_id}", payload=payload, qos=1, retain=False)
        print(f"Sending {payload} to esps/{device_id}")


async def ping_pong(client, payload):
    """
    """
    device_id = 4
    payload["program"] = 'fade'
    mode = payload["program_kwargs"].get("mode", "sequential")
    duration = 2 * payload["program_kwargs"].get("duration_fade", 1)  # Up and Down
    if mode not in {'sequential', 'random', 'trailing'}:
        mode = 'sequential'
    if mode == 'trailing':
        payload["program_kwargs"]["duration_fade"] = float(duration) / 3
        payload["program_kwargs"]["duration_fade_bottom"] = 2 * float(duration) / 3
    payload_json = json.dumps(payload)
    while True:
        client.publish(topic=f"esps/{device_id}", payload=payload_json, qos=1, retain=False)
        print(f"Sending {payload} to esps/{device_id}")
        if mode == 'random':
            offset = random.randint(1, 4)  # avoid sampling twice the same
            device_id = device_id + offset % 6 + 1
        else:
            device_id = device_id % 6 + 1
        await asyncio.sleep(duration)


async def program(client, payload):
    program_name, program_kwargs = payload["program"], payload["program_kwargs"]
    payload_json = json.dumps(payload)
    if program_name == "ping_pong":
        await ping_pong(client, payload)
    if program_name in {"color_cycle", "color_flash", "storm"}:
        await broadcast_name_and_kwargs(client=client, payload=payload_json)
