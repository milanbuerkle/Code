from machine import Pin
import time

# ==========================================
# 1. PINS DEFINIEREN (Konstanten)
# ==========================================
PIN_LED_RED1    = 5
PIN_LED_RED2    = 18
PIN_LED_GREEN1  = 19
PIN_LED_GREEN2  = 21
PIN_LED_YELLOW  = 22
PIN_LED_SPECIAL = 23  # Blau / Weiß

PIN_BTN1        = 13
PIN_BTN2        = 12
PIN_SENSOR      = 14  # Lichtschranke / Digitaler Sensor

# ==========================================
# 2. HARDWARE INITIALISIEREN
# ==========================================
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

# ==========================================
# 3. HILFSFUNKTIONEN & ZUSTÄNDE
# ==========================================
def all_leds_off():
    led_red1.off()
    led_red2.off()
    led_green1.off()
    led_green2.off()
    led_yellow.off()
    led_special.off()

# Zustände definieren
STATE_IDLE     = 0
STATE_ACTIVE   = 1
STATE_BLINKING = 2
STATE_ERROR    = 3

current_state = STATE_IDLE

# Timer & Flanken-Speicher
start_time = 0
last_blink_time = time.ticks_ms()
blink_state = False

last_btn1_val   = btn1.value()
last_btn2_val   = btn2.value()
last_sensor_val = sensor.value()

print("System gestartet. Bereit für die Live-Demo!")

# ==========================================
# 4. HAUPTSCHLEIFE (STATE MACHINE)
# ==========================================
while True:
    now = time.ticks_ms()

    # --- A) EINGÄNGE EINLESEN ---
    btn1_val   = btn1.value()
    btn2_val   = btn2.value()
    sensor_val = sensor.value()

    # --- B) FLANKENERKENNUNG (Falling Edge) ---
    btn1_pressed     = (btn1_val == 0 and last_btn1_val == 1)
    btn2_pressed     = (btn2_val == 0 and last_btn2_val == 1)
    sensor_triggered = (sensor_val == 0 and last_sensor_val == 1)  # Lichtschranke unterbrochen

    # --- C) TRANSITIONS (Zustandsübergänge) ---
    if current_state == STATE_IDLE:
        # Taster 1 oder Lichtschranke startet den Ablauf
        if btn1_pressed or sensor_triggered:
            current_state = STATE_ACTIVE
            start_time = now
            print("Zustand: IDLE -> ACTIVE")

    elif current_state == STATE_ACTIVE:
        # Nach 3000 ms weiter zu BLINKING
        if time.ticks_diff(now, start_time) >= 3000:
            current_state = STATE_BLINKING
            start_time = now
            print("Zustand: ACTIVE -> BLINKING")
        elif btn2_pressed:
            current_state = STATE_ERROR
            print("Zustand: ACTIVE -> ERROR")

    elif current_state == STATE_BLINKING:
        # Nach 5000 ms zurück zu IDLE
        if time.ticks_diff(now, start_time) >= 5000:
            current_state = STATE_IDLE
            print("Zustand: BLINKING -> IDLE")

    elif current_state == STATE_ERROR:
        # Taster 2 quittiert den Fehler
        if btn2_pressed:
            current_state = STATE_IDLE
            print("Fehler quittiert -> IDLE")

    # --- D) AKTIONEN (Ausgänge / LEDs schalten) ---
    all_leds_off()

    # Nicht-blockierender Blink-Taktgeber (alle 250 ms umschalten)
    if time.ticks_diff(now, last_blink_time) >= 250:
        blink_state = not blink_state
        last_blink_time = now

    if current_state == STATE_IDLE:
        led_green1.on()
        led_red1.on()

    elif current_state == STATE_ACTIVE:
        led_yellow.on()
        led_green2.on()

    elif current_state == STATE_BLINKING:
        if blink_state:
            led_yellow.on()
        led_special.on()

    elif current_state == STATE_ERROR:
        if blink_state:
            led_red1.on()
            led_red2.on()

    # --- E) FLANKEN-SPEICHER AKTUALISIEREN ---
    last_btn1_val   = btn1_val
    last_btn2_val   = btn2_val
    last_sensor_val = sensor_val