from machine import Pin
import time

# 1. PINS DEFINIEREN (Konstanten)
PIN_LED_RED1    = 15 #auto
PIN_LED_RED2    = 27 #ped
PIN_LED_GREEN1  = 5
PIN_LED_GREEN2  = 14
PIN_LED_YELLOW  = 4
PIN_LED_SPECIAL = 12 

PIN_BTN1        = 21
PIN_BTN2        = 23
PIN_SENSOR      = 13

# 2. HARDWARE INITIALISIEREN
led_red1    = Pin(PIN_LED_RED1, Pin.OUT, value=0)
led_red2    = Pin(PIN_LED_RED2, Pin.OUT, value=0)
led_green1  = Pin(PIN_LED_GREEN1, Pin.OUT, value=0)
led_green2  = Pin(PIN_LED_GREEN2, Pin.OUT, value=0)
led_yellow  = Pin(PIN_LED_YELLOW, Pin.OUT, value=0)
led_special = Pin(PIN_LED_SPECIAL, Pin.OUT, value=0)

# Eingänge mit Pull-Up (Ungedrückt = 1, Gedrückt / Ausgelöst = 0)
btn1   = Pin(PIN_BTN1, Pin.IN, Pin.PULL_UP)
btn2   = Pin(PIN_BTN2, Pin.IN, Pin.PULL_UP)
sensor = Pin(PIN_SENSOR, Pin.IN, Pin.PULL_UP)

# 3. STATI & ZUSTÄNDE DEFINIEREN

STATE_CAR_RED     = 0
STATE_CAR_YELLOW_TO_RED   = 1
STATE_CAR_GREEN_BLINK = 2
STATE_CAR_GREEN    = 3
STATE_PED_RED = STATE_CAR_GREEN
STATE_BLUE_ON = 4
STATE_CAR_YELLOW_TO_GREEN   = 5

current_state = STATE_CAR_GREEN

# Timer, Entprell- & Flanken-Speicher
start_time = 0
last_blink_time = time.ticks_ms()
blink_state = False

ENTPRELL_MS = 30

btn1_roh_alt   = btn1.value()
btn1_stabil    = btn1_roh_alt
btn1_t_wechsel = time.ticks_ms()

last_sensor_val = sensor.value()

# ==========================================
# 4. HILFSFUNKTIONEN
# ==========================================
def all_leds_off():
    led_red1.off()
    led_red2.off()
    led_green1.off()
    led_green2.off()
    led_yellow.off()
    led_special.off()


# 5. FUNKTION 1: ZUSTANDSWECHSEL (TRANSITIONS)

def update_state(now, btn1_pressed, sensor_triggered):
    global current_state, start_time

    # <<< HIER ANPASSEN: Regeln für den Zustandswechsel
    if current_state == STATE_CAR_GREEN:
        # Bedingung für Wechsel zu ACTIVE (z. B. Taster oder Sensor)
        if btn1_pressed:
            current_state = STATE_CAR_GREEN_BLINK
            start_time = now  # Stoppuhr für neuen Zustand starten!
            print("Grun blinkt")


    elif current_state == STATE_CAR_GREEN_BLINK:
        # <<< HIER ANPASSEN: Zeitdauer in Millisekunden (z. B. 3000 = 3 Sek)
        if time.ticks_diff(now, start_time) >= 5000:
            current_state = STATE_CAR_YELLOW_TO_RED
            start_time = now  # Stoppuhr neu starten!
            print("Gelb an")

    elif current_state == STATE_CAR_YELLOW_TO_RED:
         if time.ticks_diff(now, start_time) >= 1000:
            current_state = STATE_CAR_RED
            start_time = now
            print("Rot an")
    
    elif current_state == STATE_CAR_RED:
        # 1. Wenn der Sensor gedrückt/ausgelöst wird, merkst du dir die Startzeit!
        if sensor_triggered:
            current_state = STATE_CAR_YELLOW_TO_GREEN
            start_time = now
            
    elif current_state == STATE_CAR_YELLOW_TO_GREEN:
        if time.ticks_diff(now, start_time) >= 3000:
            current_state = STATE_CAR_GREEN
# ==========================================
def execute_actions(now):
    global last_blink_time, blink_state

    all_leds_off()  # Zuerst alle LEDs zurücksetzen


    if time.ticks_diff(now, last_blink_time) >= 500:
        blink_state = not blink_state
        last_blink_time = now


    if current_state == STATE_CAR_GREEN:
        led_green1.on()
        led_red2.on()

    elif current_state == STATE_CAR_RED:
        led_red1.on()
        led_green2.on()

    elif current_state == STATE_CAR_GREEN_BLINK:
        led_red2.on()
        if blink_state:
            led_green1.on()
        

    elif current_state == STATE_CAR_YELLOW_TO_RED:
        led_yellow.on()
        led_red2.on()
    
    elif current_state == STATE_CAR_YELLOW_TO_GREEN:
        led_yellow.on()
        led_red2.on()
        led_red1.on()
        
    elif current_state == STATE_CAR_RED:
        led_red1.on()

# ==========================================
# 7. HAUPTSCHLEIFE (STATE MACHINE)
# ==========================================
print("System gestartet. Bereit fur die Live-Demo!")

while True:
    jetzt = time.ticks_ms()
    btn1_pressed = False

    # --- ENTPRELL-BLOCK FÜR BTN1 ---
    roh = btn1.value()
    
    if roh != btn1_roh_alt:  # Pegel hat sich geändert
        btn1_roh_alt = roh
        btn1_t_wechsel = jetzt  # Stoppuhr neu starten
        
    if roh != btn1_stabil:
        if time.ticks_diff(jetzt, btn1_t_wechsel) >= ENTPRELL_MS:
            btn1_stabil = roh
          
            if btn1_stabil == 0:  
                btn1_pressed = True


    # --- SENSOR ABFRAGE ---
    sensor_val = sensor.value()
    # <<< HIER ANPASSEN: Flankenerkennung für Lichtschranke (0 = unterbrochen)
    sensor_triggered = (sensor_val == 0 and last_sensor_val == 1)

    # --- FUNKTIONSAUFRUFE ---
    update_state(jetzt, btn1_pressed, sensor_triggered)
    execute_actions(jetzt)

    # --- FLANKEN-SPEICHER AKTUALISIEREN ---
    last_sensor_val = sensor_val
    
