import uasyncio as asyncio
import time
from machine import Timer, Pin, ADC, PWM
import network
from config import WIFI_SSID,WIFI_PASS
from umqtt.robust import MQTTClient


#lamp = Pin(25, Pin.OUT)
sw1 = Pin(16, Pin.IN, Pin.PULL_UP)
sw2 = Pin(14, Pin.IN, Pin.PULL_UP)
led_red = Pin(2,Pin.OUT)
led_green = Pin(12, Pin.OUT)

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
    count_sum = 0
    while True:
        # wait until sw is pressed
        while sw2.value() == 1:
            await asyncio.sleep_ms(200)
            
        # toggle LED
        count_sum = count_sum + 1
        led_green.value(1-led_green.value())
        mqtt.publish(b"daq2021/midterm/6210546676/count",count_sum)
               
            
        # wait until sw1 is released
        while sw2.value() == 0:
            await asyncio.sleep_ms(800)


def sub_callback(topic,payload):
    if topic == b"daq2021/midterm/6210546676/count":
        try:
            payload = int(payload.decode())
            print(payload)
        except ValueError:
            pass


        
    
mqtt.set_callback(sub_callback)
#mqtt.subscribe(b"daq2021/midterm/6210546676/count")
mqtt.subscribe(b"daq2021/midterm/6210546676/blink")

async def check_mqtt():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)


# create and run coroutines
loop = asyncio.get_event_loop()
loop.create_task(check_mqtt())
loop.create_task(switch_toggle())
loop.run_forever()




