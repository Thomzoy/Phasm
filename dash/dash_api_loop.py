import asyncio
import dash_programs

import dash_mqtt
import json

PAYLOAD = dict(
    program="storm",
    program_kwargs={},
)
CHANGE_PROGRAM = False

CURRENT_TASK = None

def on_message(client, userdata, message):
    global PAYLOAD, CHANGE_PROGRAM, CURRENT_TASK
    CHANGE_PROGRAM = True
    topic = message.topic
    msg = message.payload
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    PAYLOAD = json.loads(msg.decode("utf-8"))
    print("Payload: ", PAYLOAD)
    try:
        CURRENT_TASK.cancel()
    except:
        pass
    #dash_programs.program(client, payload)

def callback(topic, msg, retained):
    global client, PAYLOAD
    print((topic, msg, retained))
    payload = json.loads(msg.decode("utf-8"))
    print("Payload: ", payload)
    PAYLOAD = payload

async def main():
    global PAYLOAD, CHANGE_PROGRAM, CURRENT_TASK
    while True:
        if CHANGE_PROGRAM:
            print("Changing program: ", PAYLOAD)
            CURRENT_TASK = asyncio.create_task(
                dash_programs.program(client, PAYLOAD)
            )
            CHANGE_PROGRAM = False
            try:
                await CURRENT_TASK
            except asyncio.CancelledError as e:
                print(e)
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
    client.loop_start()
    asyncio.run(main())
