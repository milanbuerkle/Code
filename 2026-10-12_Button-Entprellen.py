from machine import Pin
import time

LED_PIN = 15
BUTTON_PIN = 2

# Hilfreich bei Simulatio in Wokwi
print("Hello ESP")

led_pin = Pin(LED_PIN, Pin.OUT, value=0)
button_pin = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

last_state = button_pin.value()

while True:
    # Viele Ausgaben, da viele Schleifendurchläufe
    # während der Button gedrückt wird
    # if button_pin.value() == 0:
    #     print("Button gedrückt!")


    # Fallende Flanke erkennen
    # Trotzdem mehrere Ausgaben, weil Button prellt
    current_state = button_pin.value()
    if current_state == 0 and current_state != last_state:
        # Fallende Flanke erkennen
        print("Button gedrückt!")

    