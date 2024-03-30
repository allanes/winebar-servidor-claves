from pydantic import BaseModel
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
class RaspiPinConfig(BaseModel):
    rs: int = 25 
    en: int = 24
    d4: int = 23
    d5: int = 17
    d6: int = 18
    d7: int = 22
    backlight: int  = 4
    cols:int = 20
    lines: int = 4

raspi_pin_config = RaspiPinConfig()

lcd = LCD.Adafruit_CharLCD(**raspi_pin_config.model_dump())