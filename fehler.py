if current_state == STATE_CAR_GO:
    if ped_requested:
        current_state = STATE_CAR_YELLOW
        start_time = now  # <--- WICHTIG! Stoppuhr für GELB startet JETZT.


        ⚠️ Fehler 2: Falsche Klammern oder Reihenfolge bei time.ticks_diff()
Erinnere dich immer an die Regel: time.ticks_diff(jetzt, damals).

now (oder time.ticks_ms()) steht vorne.

start_time steht hinten.

Keine doppelten Klammern am Ende machen ()) ist ein Syntaxfehler).
