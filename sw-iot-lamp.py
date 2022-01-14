import uasyncio as asyncio
import time
from machine import Timer, Pin, ADC, PWM
import network
from config import WIFI_SSID,WIFI_PASS
from umqtt.robust import MQTTClient


lamp = Pin(25, Pin.OUT)
sw1 = Pin(14, Pin.IN, Pin.PULL_UP)


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


async def switch_toggle():
    while True:
        # wait until sw is pressed
        while sw1.value() == 1:
            await asyncio.sleep_ms(0)
            
        # toggle LED
        b1 = lamp.value(1-lamp.value())
        mqtt.publish(b"daq2021/midterm/6210546676/count",b1)
            
        # wait until sw1 is released
        while sw1.value() == 0:
            await asyncio.sleep_ms(0)


def sub_callback(topic,payload):
    if topic == b"daq2021/midterm/6210546676/count":
        try:
            payload = int(payload.decode())
            print(payload)
            if payload == 0:
                lamp.value(1)
            if payload == 1:
                lamp.value(0)
        except ValueError:
            pass


        
    
mqtt.set_callback(sub_callback)
mqtt.subscribe(b"daq2021/midterm/6210546676/count")

async def check_mqtt():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)


# create and run coroutines
loop = asyncio.get_event_loop()
loop.create_task(check_mqtt())
loop.create_task(switch_toggle())
loop.run_forever()