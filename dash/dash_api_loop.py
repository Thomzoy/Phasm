import asyncio
import dash_programs

import dash_mqtt
import json


def callback(topic, msg, retained):
    global client
    print((topic, msg, retained))
    payload = json.loads(msg.decode("utf-8"))
    print("Payload: ", payload)
    dash_programs.program(client, payload)


async def main():
    while True:
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    # My PC
    HOST = "127.0.0.1"
    PORT = 1883

    # # Pi
    # HOST = "10.3.141.1"
    # PORT = 8000

    client = dash_mqtt.get_client(host_address=HOST, port=PORT)
    client.subscribe("dash/main", 1)
    client.subscribe("esps/1", 1)
    client.subscribe("esps/2", 1)
    client.subscribe("esps/3", 1)
    client.subscribe("esps/4", 1)
    print('done subscribing')
    client.loop_forever()
    # asyncio.run(main())
