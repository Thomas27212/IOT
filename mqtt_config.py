import requests
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
NTFY = "https://ntfy.sh/acrylic-ecole-7k42x9qz"

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    requests.post(NTFY, data=msg.payload, headers={"Title": msg.topic, "Priority": "high", "Tags": "rotating_light"}, timeout=10)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe("maison/+/alerte")
client.loop_forever()