import threading
from evdev import InputDevice, categorize, ecodes, list_devices
from pydantic import BaseModel

# Store the card data and associated phys_port
class DatosLectorUsado(BaseModel):
    rfid: int
    phys: str

card_data:DatosLectorUsado = None

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

def get_saved_phys_port(card_number: int) -> str:
    global card_data
    if card_data is None:
        return None
    if card_data.rfid != card_number:
        return None
    
    phys_port = card_data.phys
    card_data = None
    return phys_port

def capture_rfid_data(reader_path: str):
    reader_device = InputDevice(reader_path)
    print(f"Capturing RFID card data from reader: {reader_device.phys}")
    
    card_number = ""
    while True:
        for event in reader_device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code == ecodes.KEY_ENTER:
                    if card_number:
                        save_card_data(card_number, reader_device.phys)
                        card_number = ""
                else:
                    card_number += categorize(event).keycode[len("KEY_"):]

def save_card_data(card_number, phys_port):
    global card_data
    card_data = DatosLectorUsado(
        rfid = card_number,
        phys = phys_port
    )
    # print(f'Tarjeta leida {card_data.rfid} desde puerto: {card_data.phys} guardada')

def start_rfid_capture():
    for keyboard in get_keyboards():
        threading.Thread(
            target=capture_rfid_data, args=(keyboard.path,)
        ).start()