import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

WIFI = "NomDeTonWifi"
MDP = "MotDePasseWifi"
BROKER = "192.168.1.50"
TOPIC = b"maison/alarme/alerte"

pir = Pin(13, Pin.IN)
trig = Pin(5, Pin.OUT)
echo = Pin(35, Pin.IN)
porte = Pin(27, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

w = network.WLAN(network.STA_IF)
w.active(True)
w.connect(WIFI, MDP)
while not w.isconnected():
    time.sleep(1)
print(w.ifconfig())

client = MQTTClient("esp32-alarme", BROKER)
client.connect()
client.publish(b"maison/alarme/etat", b"alarme en ligne")

def distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time.ticks_us()
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), t) > 30000:
            return -1
    debut = time.ticks_us()
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), debut) > 30000:
            return -1
    return time.ticks_diff(time.ticks_us(), debut) / 58

dernier = 0
while True:
    d = distance()
    texte = ""
    if porte.value() == 1:
        texte = "Porte ouverte"
    elif pir.value() == 1:
        texte = "Mouvement detecte"
    elif d > 0 and d < 60:
        texte = "Presence a " + str(int(d)) + " cm"
    if texte != "" and time.time() - dernier > 30:
        try:
            client.publish(TOPIC, texte)
        except OSError:
            client.connect()
        led.value(1)
        dernier = time.time()
        time.sleep(1)
        led.value(0)
    time.sleep(0.2)