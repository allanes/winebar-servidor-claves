# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
from pin_config import *
import Adafruit_CharLCD as LCD
from funciones_lcd import (
    print_one_line_message
)

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows, lcd_backlight
)

print_one_line_message(lcd, 'Cami', line=2)

