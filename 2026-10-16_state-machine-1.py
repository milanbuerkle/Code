from machine import Pin
import time

# Pins
PIN_BUTTON_OFF = 4
PIN_BUTTON_ON = 2
PIN_LED = 15

# Hardware
btn_off = Pin(PIN_BUTTON_OFF, Pin.IN, Pin.PULL_UP)
btn_on = Pin(PIN_BUTTON_ON, Pin.IN, Pin.PULL_UP)
led = Pin(PIN_LED, Pin.OUT)

# State Machine
STATE_OFF = 0
STATE_ON = 1
current_state = STATE_OFF

last_btn_off_state = btn_off.value()
last_btn_on_state = btn_on.value()

while True:
    btn_off_value = btn_off.value()
    btn_on_value = btn_on.value()
    
    # Transitions / Übergänge
    if current_state == STATE_OFF:
        if btn_on_value == 0 and btn_on_value != last_btn_on_state:
            current_state = STATE_ON
            print("off -> on")
    elif current_state == STATE_ON:
        if btn_off_value == 0 and btn_off_value != last_btn_off_state:
            current_state = STATE_OFF
            print("on -> off")

    # Aktionen
    if current_state == STATE_OFF:
        led.off()
    elif current_state == STATE_ON:
        led.on()
    
    last_btn_off_state = btn_off_value
    last_btn_on_state = btn_on_value