from evdev import InputDevice, list_devices, ecodes, categorize
from pydantic import BaseModel

class CardInfo(BaseModel):
    card_number: int
    phys_port: str

def get_keyboards() -> list[InputDevice]:
    devices = [InputDevice(path) for path in list_devices()]
    rfid_keyboards = []
    for device in devices:
        if device.name.find('RFID') >= 0:
            if device.name.find('Keyboard') >= 0:
                rfid_keyboards.append(device)
    print(f'Se detectaron {len(rfid_keyboards)} lectores RFID')
    return rfid_keyboards

def get_keyboard_ports() -> list[str]:
    devices = get_keyboards()
    puertos = [device.phys for device in devices]
    return puertos

def read_card(device: InputDevice) -> str:
    card_number = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            if event.code == ecodes.KEY_ENTER:
                return card_number.lstrip("0")
            else:
                card_number += categorize(event).keycode[len("KEY_"):]