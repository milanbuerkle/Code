from machine import Pin
import time

LED_PIN = 15
BUTTON_PIN = 2

# Hilfreich bei Simulatio in Wokwi
print("Hello ESP")

led_pin = Pin(LED_PIN, Pin.OUT, value=0)
button_pin = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

while True:
    led_pin.value(button_pin.value())