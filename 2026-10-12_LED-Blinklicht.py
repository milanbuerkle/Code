from machine import Pin
import time

LED_PIN = 15

# Hilfreich bei Simulatio in Wokwi
print("Hello ESP")

led_pin = Pin(LED_PIN, Pin.OUT, value=0)

while True:
    led_pin.on()
    time.sleep(0.5)
    led_pin.off()
    time.sleep(0.5)