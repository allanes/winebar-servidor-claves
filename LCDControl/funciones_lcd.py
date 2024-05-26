import time
from pydantic import BaseModel
import Adafruit_CharLCD as LCD
from .raspi_config import raspi_pin_config

class InfoCliente(BaseModel):
    nombre: str
    consumos: float
    carrito: float = 0

    def armar_mensaje(self) -> str:
        linea1 = centrar_linea('ALTACAVA WINEBAR')
        linea2 = centrar_linea(f'Hola {self.nombre}!')
        linea3 = f'Consumos: ${self.consumos:.2f}'
        linea4 = f'Carrito : ${self.carrito:.2f}'

        mensaje = linea1 + '\n' + linea2 + '\n' + linea3 + '\n' + linea4
        return mensaje

def centrar_linea(msg: str) -> str:
    columnas_sobrantes = raspi_pin_config.cols - len(msg)
    mitad_del_sobrante = columnas_sobrantes // 2
    prefijo_linea = ' ' * mitad_del_sobrante
    linea_centrada = prefijo_linea + msg
    return linea_centrada

def print_info_cliente(lcd: LCD, info: InfoCliente):
    lcd.clear()
    lcd.show_cursor(False)

    mensaje = info.armar_mensaje()
    lcd.message(mensaje)

def limpiar_pantalla(lcd: LCD):
    lcd.clear()
    linea1 = centrar_linea('ALTACAVA WINEBAR')
    linea2 = ''
    linea3 = centrar_linea('Bienvenido!')
    linea4 = ''

    mensaje_bienvenida = linea1 + '\n' + linea2 + '\n' + linea3 + '\n' + linea4

    lcd.message(mensaje_bienvenida)

def print_one_line_message(lcd: LCD, msg: str, line: int = 0):
    lcd.clear()
    lcd.show_cursor(False)
    # lcd.blink(True)
    
    if line > 3:
        line = 3

    linea = '\n' * line
    message = linea + msg[:raspi_pin_config.cols]
    lcd.message(message)

    # Wait 5 seconds
    time.sleep(5.0)

def scroll_one_line_message(lcd: LCD, msg: str):
    # Demo scrolling message right/left.
    lcd.clear()
    message = msg[:raspi_pin_config.cols]
    lcd.message(message)

    for i in range(raspi_pin_config.cols-len(message)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(raspi_pin_config.lcd_columns-len(message)):
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
