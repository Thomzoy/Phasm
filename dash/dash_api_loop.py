import asyncio
import dash_programs

import dash_mqtt
import json


def on_message(client, userdata, message):
    topic = message.topic
    msg = message.payload
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    payload = json.loads(msg.decode("utf-8"))
    print("Payload: ", payload)
    dash_programs.program(client, payload)

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
    HOST = "10.3.141.1"
    MQTT_PORT = 1883

    client = dash_mqtt.get_client(host_address=HOST, port=MQTT_PORT)
    client.subscribe("dash/main", 1)
    print('done subscribing')
    client.on_message=on_message
    client.loop_forever()
    # asyncio.run(main())
