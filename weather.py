import json
import kidbright as kb
import uasyncio as asyncio
import time
from machine import Timer, Pin, ADC, PWM
import network
from config import WIFI_SSID,WIFI_PASS
from umqtt.robust import MQTTClient

kb.init()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("*** Connecting to WiFi...")
wlan.connect(WIFI_SSID,WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
print("*** Wifi connected")

mqtt = MQTTClient("Beam-123589746","iot.cpe.ku.ac.th")
print("*** Connecting to MQTT broker...")
mqtt.connect()
print("*** MQTT broker connected")

while True:
    data = {
        'light': kb.light(),
        'temperature': kb.temperature()
    }
    mqtt.publish('ku/daq2021/6210546676/sensors',
        json.dumps(data))
    time.sleep(10)