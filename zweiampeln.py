from machine import Pin
import time


# Pins
PIN_BUTTON = 23
PIN_LED_CAR_RED = 5
PIN_LED_CAR_GREEN = 4
PIN_LED_PED_RED = 15
PIN_LED_PED_GREEN = 19

# Hardware / Bennenung
btn1 = Pin(PIN_BUTTON, Pin.IN, Pin.PULL_UP)
led_car_red = Pin(PIN_LED_CAR_RED, Pin.OUT)
led_car_green = Pin(PIN_LED_CAR_GREEN, Pin.OUT)
led_ped_red = Pin(PIN_LED_PED_RED,Pin.OUT,)
led_ped_green = Pin(PIN_LED_PED_GREEN,Pin.OUT)




# State Machine 

# Zustände definieren
STATE_CAR_RED = 0
STATE_CAR_GREEN = 1
STATE_PED_RED = 2
STATE_PED_GREEN = 3
current_state = STATE_CAR_GREEN

last_button_state = btn1.value()
start_time = 0



# Pins definieren High oder Low
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
            current_state = STATE_CAR_RED
            print("taster gedrückt, welchsle zu auto rot")
            start_time = time.ticks_ms() 
                         

    elif current_state == STATE_CAR_RED:
        if time.ticks_diff(time.ticks_ms(), start_time) >= 2000:
            current_state = STATE_PED_GREEN
            print("2s um wechsle zu fußgänger grün")
            start_time = time.ticks_ms() 

    elif current_state == STATE_PED_GREEN:
        if time.ticks_diff(time.ticks_ms(), start_time) >= 5000:
            current_state = STATE_PED_RED
            print("5s um wechsle zu fußgänger rot")
            start_time = time.ticks_ms() 
          

    elif current_state == STATE_PED_RED:
        if time.ticks_diff(time.ticks_ms(), start_time) >= 2000:  
            current_state = STATE_CAR_GREEN
            print("2s um wechsle zu auto grün")
            




    # Aktionen
    all_leds_off()
    if current_state == STATE_CAR_RED:
        led_car_red.on()

    elif current_state == STATE_CAR_GREEN:
        led_car_green.on()
            

    elif current_state == STATE_PED_RED:
        led_ped_red.on()
    
    elif current_state == STATE_PED_GREEN:
        led_ped_green.on()
             
    
    
    last_button_state = button1_value

y