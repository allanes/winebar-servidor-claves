# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
from raspi_config import lcd
import Adafruit_CharLCD as LCD
from funciones_lcd import (
    print_one_line_message,
    print_info_cliente,
    InfoCliente
)

# print_one_line_message(lcd, 'Cami', line=2)

info_cliente = InfoCliente(
    nombre = 'Adrian',
    consumos = 10000,
    carrito = 5000
)

print_info_cliente(lcd, info_cliente)