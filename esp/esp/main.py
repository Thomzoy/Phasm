import time
from mqtt_as import MQTTClient, config
import uasyncio as asyncio

from configuration import COLORS, PROGRAM

import helpers as h
import programs as p

import json


def callback(topic, msg, retained):

    global PROGRAM

    print((topic, msg, retained))
    payload = json.loads(msg.decode("utf-8"))
    print("Payload: ", payload)

    PROGRAM["current_program"] = payload["program"]
    PROGRAM["program_kwargs"] = payload["program_kwargs"]
    print("Updated program: ", PROGRAM)


async def conn_han(client):
    await client.subscribe("tpj_test_topic", 1)


async def main(client):

    h.reset_pins()
    global PROGRAM

    await client.connect()

    while True:
        await p.program(PROGRAM["current_program"], **PROGRAM["program_kwargs"])
        print(PROGRAM)


config["subs_cb"] = callback
config["connect_coro"] = conn_han

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
