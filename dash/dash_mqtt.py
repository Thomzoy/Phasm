import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test_topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('I received a message !')
    print(msg.topic + " " + str(msg.payload))


def on_publish(client, userdata, msg):
    print('I published a message !')
    print(msg.topic + " " + str(msg.payload))


def get_client(host_address="10.3.141.1", port=1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_publish = on_publish
    client.connect(host=host_address, port=port, keepalive=60)
    print("Connected")

    return client
