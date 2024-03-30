import time
import Adafruit_CharLCD as LCD
from pin_config import *

def print_one_line_message(lcd: LCD, msg: str, line: int = 0):
    lcd.clear()
    lcd.show_cursor(False)
    # lcd.blink(True)
    
    if line > 3:
        line = 3

    linea = '\n' * line
    message = linea + msg[:lcd_columns]
    lcd.message(message)

    # Wait 5 seconds
    time.sleep(5.0)

def scroll_one_line_message(lcd: LCD, msg: str):
    # Demo scrolling message right/left.
    lcd.clear()
    message = msg[:lcd_columns]
    lcd.message(message)

    for i in range(lcd_columns-len(message)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(lcd_columns-len(message)):
        time.sleep(0.5)
        lcd.move_left()

# # Demo turning backlight off and on.
# lcd.clear()
# lcd.message('Flash backlight\nin 5 seconds...')
# time.sleep(5.0)
# # Turn backlight off.
# lcd.set_backlight(0)
# time.sleep(2.0)
# # Change message.
# lcd.clear()
# lcd.message('Goodbye!')
# # Turn backlight on.
# lcd.set_backlight(1)
