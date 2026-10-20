from machine import Pin
import time

led = Pin(2, Pin.OUT)

def time_passed(since, duration):
    return time.ticks_diff(time.ticks_ms(), since) >= duration

last_toggle = time.ticks_ms()

while True:
    if time_passed(last_toggle, 200):
        led.value(not led.value())
        last_toggle = time.ticks_ms()
