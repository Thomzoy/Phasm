import json
import time
import asyncio

# This is meant to be used by the main in dash.

async def broadcast_name_and_kwargs(client, payload):
    """
    To simulate a storm each "flash_period" seconds
    """
    for device_id in range(1, 6):
        #client.publish(topic=f"esps/{device_id}", payload=payload, qos=1, retain=True)
        client.publish(f"esps/{device_id}", payload=payload, qos=1, retain=False)
        print(f"Sending {payload} to esps/{device_id}")


async def ping_pong(client, payload):
    """
    To simulate a storm each "flash_period" seconds
    """
    device_id = 4
    payload["program"] = 'fade'
    duration=2*payload["program_kwargs"].get("duration_fade",1) # Up and Down
    payload_json = json.dumps(payload)
    while True:
        client.publish(topic=f"esps/{device_id}", payload=payload_json, qos=1, retain=False)
        print(f"Sending {payload} to esps/{device_id}")
        device_id = device_id % 6 + 1
        await asyncio.sleep(duration)



async def program(client, payload):
    program_name, program_kwargs = payload["program"], payload["program_kwargs"]
    payload_json = json.dumps(payload)
    if program_name == "ping_pong":
        await ping_pong(client, payload)
    if program_name in {"color_cycle", "color_flash","storm"}:
        await broadcast_name_and_kwargs(client=client, payload=payload_json)
