from machine import UART, Pin

# definice UART komunikace, výstupy, vstupy, rychlost přenosu
uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=5000)