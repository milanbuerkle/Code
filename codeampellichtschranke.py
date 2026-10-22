from machine import Pin
import time

# ==========================================
# 1. PINS DEFINIEREN (Konstanten)
# ==========================================
PIN_CAR_RED     = 5
PIN_CAR_YELLOW  = 22
PIN_CAR_GREEN   = 4
PIN_PED_RED     = 18
PIN_PED_GREEN   = 19
PIN_LED_SPECIAL = 23  # Blau/Sonder-Anzeige (z. B. "Anforderung gespeichert")

PIN_BTN_PED     = 13  # Taster 1: Fußgänger-Taste
PIN_BTN_RESET   = 12  # Taster 2: Reset / Service-Taste
PIN_CAR_SENSOR  = 14  # Lichtschranke / Induktionsschleife (Auto kommt)

# ==========================================
# 2. HARDWARE INITIALISIEREN
# ==========================================
led_car_red    = Pin(PIN_CAR_RED, Pin.OUT, value=0)
led_car_yellow = Pin(PIN_CAR_YELLOW, Pin.OUT, value=0)
led_car_green  = Pin(PIN_CAR_GREEN, Pin.OUT, value=0)
led_ped_red    = Pin(PIN_PED_RED, Pin.OUT, value=0)
led_ped_green  = Pin(PIN_PED_GREEN, Pin.OUT, value=0)
led_special    = Pin(PIN_LED_SPECIAL, Pin.OUT, value=0)

btn_ped    = Pin(PIN_BTN_PED, Pin.IN, Pin.PULL_UP)
btn_reset  = Pin(PIN_BTN_RESET, Pin.IN, Pin.PULL_UP)
car_sensor = Pin(PIN_CAR_SENSOR, Pin.IN, Pin.PULL_UP)

# ==========================================
# 3. HILFSFUNKTIONEN & ZUSTÄNDE
# ==========================================
def all_leds_off():
    led_car_red.off()
    led_car_yellow.off()
    led_car_green.off()
    led_ped_red.off()
    led_ped_green.off()
    led_special.off()

# Zustände der Ampel
STATE_CAR_GO     = 0  # Autos Grün, Fußgänger Rot
STATE_CAR_YELLOW = 1  # Autos Gelb
STATE_ALL_RED    = 2  # Sicherheitsphase: Beide Rot
STATE_PED_GO     = 3  # Fußgänger Grün
STATE_SERVICE    = 4  # Gelb-Blinken (Wartung/Fehler)

current_state = STATE_CAR_GO

start_time = 0
last_blink_time = time.ticks_ms()
blink_state = False

last_btn_ped_val   = btn_ped.value()
last_btn_reset_val = btn_reset.value()
last_sensor_val    = car_sensor.value()

ped_requested = False  # Speichert den Fußgänger-Tastendruck

# ==========================================
# 4. HAUPTSCHLEIFE (STATE MACHINE)
# ==========================================
while True:
    now = time.ticks_ms()

    # --- A) EINGÄNGE EINLESEN ---
    btn_ped_val   = btn_ped.value()
    btn_reset_val = btn_reset.value()
    sensor_val    = car_sensor.value()

    # --- B) FLANKENERKENNUNG (Falling Edges) ---
    btn_ped_pressed   = (btn_ped_val == 0 and last_btn_ped_val == 1)
    btn_reset_pressed = (btn_reset_val == 0 and last_btn_reset_val == 1)
    car_detected      = (sensor_val == 0 and last_sensor_val == 1) # Auto fährt in Lichtschranke

    # Fußgänger-Anforderung unabhängig merken
    if btn_ped_pressed:
        ped_requested = True
        print("Fußgänger-Wunsch gespeichert!")

    # --- C) TRANSITIONS (Zustandsübergänge) ---
    if current_state == STATE_CAR_GO:
        # Wechsle zu Gelb, wenn Fußgänger gedrückt hat
        if ped_requested:
            current_state = STATE_CAR_YELLOW
            start_time = now 
            print("Autos -> GELB") 

    elif current_state == STATE_CAR_YELLOW:
        if time.ticks_diff(now, start_time) >= 2000:  # 2 Sek Gelb
            current_state = STATE_ALL_RED
            start_time = now
            print("Beide -> ROT")

    elif current_state == STATE_ALL_RED:
        if time.ticks_diff(now, start_time) >= 1000:  # 1 Sek Räumphase
            current_state = STATE_PED_GO
            start_time = now
            ped_requested = False  # Anforderung zurücksetzen
            print("Fußgänger -> GRÜN")

    elif current_state == STATE_PED_GO:
        if time.ticks_diff(now, start_time) >= 4000:  # 4 Sek Grünphase
            current_state = STATE_CAR_GO
            print("Autos -> GRÜN")

    # Manuelle Service-Taste (Taster 2) schaltet Service-Modus um
    if btn_reset_pressed:
        if current_state != STATE_SERVICE:
            current_state = STATE_SERVICE
            print("Modus: SERVICE (Blinken)")
        else:
            current_state = STATE_CAR_GO
            print("Modus: NORMAL (Auto Grün)")

    # --- D) AKTIONEN (LEDs schalten) ---
    all_leds_off()

    # Nicht-blockierender Blinktakt (alle 500 ms)
    if time.ticks_diff(now, last_blink_time) >= 500:
        blink_state = not blink_state
        last_blink_time = now

    if current_state == STATE_CAR_GO:
        led_car_green.on()
        led_ped_red.on()

    elif current_state == STATE_CAR_YELLOW:
        led_car_yellow.on()
        led_ped_red.on()

    elif current_state == STATE_ALL_RED:
        led_car_red.on()
        led_ped_red.on()

    elif current_state == STATE_PED_GO:
        led_car_red.on()
        led_ped_green.on()

    elif current_state == STATE_SERVICE:
        if blink_state:
            led_car_yellow.on()

    # Blaue/Sonder-LED leuchtet, solange Anforderung aktiv ist
    if ped_requested and current_state != STATE_PED_GO:
        led_special.on()

    # --- E) FLANKEN-SPEICHER AKTUALISIEREN ---
    last_btn_ped_val   = btn_ped_val
    last_btn_reset_val = btn_reset_val
    last_sensor_val    = sensor_val