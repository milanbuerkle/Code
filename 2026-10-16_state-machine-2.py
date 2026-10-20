from machine import Pin
import time

# Pins
PIN_BUTTON = 4
PIN_LED_CAR_RED = 23
PIN_LED_CAR_GREEN = 21
PIN_LED_PED_RED = 21
PIN_LED_PED_GREEN = 19

# Hardware
btn1 = Pin(PIN_BUTTON, Pin.IN, Pin.PULL_UP)
led_car_red = Pin(PIN_LED_CAR_RED, Pin.OUT)
led_car_green = Pin(PIN_LED_CAR_GREEN, Pin.OUT)
led_ped_red = Pin(PIN_LED_PED_RED, Pin.OUT)
led_ped_green = Pin(PIN_LED_PED_GREEN, Pin.OUT)

# State Machine
STATE_CAR_GREEN = 0
STATE_ALL_RED_1 = 1
STATE_PED_GREEN = 2
STATE_ALL_RED_2 = 3
current_state = STATE_CAR_GREEN

last_button_state = btn1.value()
start_time = 0

def all_leds_off():
    led_car_red.off()
    led_car_green.off()
    led_ped_red.off()
    led_ped_green.off()

while True:
    button1_value = btn1.value()
    # Transitions / Übergänge
    if current_state == STATE_CAR_GREEN:
        if button1_value == 0 and button1_value != last_button_state:
            current_state = STATE_ALL_RED_1
            print("car green -> all red 1")
            start_time = time.ticks_ms()
    elif current_state == STATE_ALL_RED_1:
        if time.ticks_diff(start_time, time.ticks_ms()) >= 1000:
            current_state = STATE_PED_GREEN
            print("all red 1 -> ped green")
            start_time = time.ticks_ms()
    elif current_state == STATE_PED_GREEN:
        if time.ticks_diff(start_time, time.ticks_ms()) >= 4000:
            current_state = STATE_ALL_RED_2
            print("ped green -> all red 2")
            start_time = time.ticks_ms()
    elif current_state == STATE_ALL_RED_2:
        if time.ticks_diff(start_time, time.ticks_ms()) >= 1000:
            current_state = STATE_CAR_GREEN
            print("all red 2 -> car green")

    # Aktionen
    if current_state == STATE_CAR_GREEN:
        all_leds_off()
        led_car_green.on()
        led_ped_red.on()
    elif current_state == STATE_ALL_RED_1 or current_state == STATE_ALL_RED_2:
        all_leds_off()
        led_car_red.on()
        led_ped_red.on()
    elif current_state == STATE_PED_GREEN:
        all_leds_off()
        led_car_red.on()
        led_ped_green.on()
    
    last_button_state = button1_value