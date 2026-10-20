from machine import Pin

BARRIER_PIN = 5

barrier = Pin(BARRIER_PIN, Pin.IN, Pin.PULL_DOWN)

while True:
    print(barrier.value())
    time.sleep(0.5)
    g