from machine import Pin
import time

led = Pin(2, Pin.OUT)
led2 = Pin(4, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP)

last_toggle = time.ticks_ms()

while True:
    now = time.ticks_ms()

    # Task 1: blink every 200 ms
    if time.ticks_diff(now, last_toggle) >= 200:
        led.value(not led.value())
        last_toggle = now

    # Task 2: react immediately to the button
    led2.value(not button.value())