from machine import Pin

LED_PIN = 15

# Hilfreich bei Simulatio in Wokwi
print("Hello ESP")

led_pin = Pin(LED_PIN, Pin.OUT, value=0)

# led_pin.on()
# led_pin.off()
led_pin.value(1)