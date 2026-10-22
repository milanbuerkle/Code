from machine import Pin
import time

# ==========================================
# 1. PINS DEFINIEREN (Konstanten)
# ==========================================
# <<< HIER ANPASSEN: Pin-Nummern laut deiner Steckbrett-Schaltung eintragen
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
# 3. STATI & ZUSTÄNDE DEFINIEREN
# ==========================================
# <<< HIER ANPASSEN: Namen & Anzahl deiner Zustände festlegen
STATE_IDLE     = 0
STATE_ACTIVE   = 1
STATE_BLINKING = 2
STATE_ERROR    = 3

# <<< HIER ANPASSEN: Welcher Zustand soll beim Start aktiv sein?
current_state = STATE_IDLE

# Timer, Entprell- & Flanken-Speicher
start_time = 0
last_blink_time = time.ticks_ms()
blink_state = False

# <<< HIER ANPASSEN: Entprellzeit falls nötig (30 ms ist Standard)
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

# ==========================================
# 5. FUNKTION 1: ZUSTANDSWECHSEL (TRANSITIONS)
# ==========================================
def update_state(now, btn1_pressed, sensor_triggered):
    global current_state, start_time

    # <<< HIER ANPASSEN: Regeln für den Zustandswechsel
    if current_state == STATE_IDLE:
        # Bedingung für Wechsel zu ACTIVE (z. B. Taster oder Sensor)
        if btn1_pressed or sensor_triggered:
            current_state = STATE_ACTIVE
            start_time = now  # Stoppuhr für neuen Zustand starten!
            print("Zustand gewechselt: IDLE -> ACTIVE")

    elif current_state == STATE_ACTIVE:
        # <<< HIER ANPASSEN: Zeitdauer in Millisekunden (z. B. 3000 = 3 Sek)
        if time.ticks_diff(now, start_time) >= 3000:
            current_state = STATE_BLINKING
            start_time = now  # Stoppuhr neu starten!
            print("Zustand gewechselt: ACTIVE -> BLINKING")

    elif current_state == STATE_BLINKING:
        # <<< HIER ANPASSEN: Zeitdauer in Millisekunden (z. B. 5000 = 5 Sek)
        if time.ticks_diff(now, start_time) >= 5000:
            current_state = STATE_IDLE
            print("Zustand gewechselt: BLINKING -> IDLE")

# ==========================================
# 6. FUNKTION 2: AKTIONEN (LEDS SCHALTEN)
# ==========================================
def execute_actions(now):
    global last_blink_time, blink_state

    all_leds_off()  # Zuerst alle LEDs zurücksetzen

    # <<< HIER ANPASSEN: Blink-Frequenz in ms (z. B. 250 ms = 4x pro Sekunde)
    if time.ticks_diff(now, last_blink_time) >= 250:
        blink_state = not blink_state
        last_blink_time = now

    # <<< HIER ANPASSEN: Welches Signal leuchtet in welchem Zustand?
    if current_state == STATE_IDLE:
        led_green1.on()
        led_red1.on()

    elif current_state == STATE_ACTIVE:
        led_yellow.on()
        led_green2.on()

    elif current_state == STATE_BLINKING:
        if blink_state:
            led_yellow.on()  # Blinken!
        led_special.on()

    elif current_state == STATE_ERROR:
        if blink_state:
            led_red1.on()
            led_red2.on()

# ==========================================
# 7. HAUPTSCHLEIFE (STATE MACHINE)
# ==========================================
print("System gestartet. Bereit für die Live-Demo!")

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
            # <<< HIER ANPASSEN: == 0 bei PULL_UP (Drücken), == 1 bei PULL_DOWN
            if btn1_stabil == 0:  
                btn1_pressed = True
                print("Taste entprellt gedrückt!")

    # --- SENSOR ABFRAGE ---
    sensor_val = sensor.value()
    # <<< HIER ANPASSEN: Flankenerkennung für Lichtschranke (0 = unterbrochen)
    sensor_triggered = (sensor_val == 0 and last_sensor_val == 1)

    # --- FUNKTIONSAUFRUFE ---
    update_state(jetzt, btn1_pressed, sensor_triggered)
    execute_actions(jetzt)

    # --- FLANKEN-SPEICHER AKTUALISIEREN ---
    last_sensor_val = sensor_val
    