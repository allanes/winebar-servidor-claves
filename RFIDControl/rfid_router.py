from fastapi import APIRouter, Depends
from .rfid_control import get_keyboards, get_keyboard_ports, read_card, CardInfo
import threading
import requests

router = APIRouter()

saved_card = None
card_read_once = False

@router.get("/keyboard_ports")
def get_ports():
    return get_keyboard_ports()

@router.get("/get_phys_port")
def get_phys_port(card_number: int):
    global saved_card, card_read_once
    if saved_card and saved_card.card_number == card_number and not card_read_once:
        card_read_once = True
        return saved_card.phys_port
    return None

def watch_keyboard(device):
    global saved_card, card_read_once
    while True:
        card_number = read_card(device)
        if not saved_card or saved_card.card_number != int(card_number):
            saved_card = CardInfo(card_number=int(card_number), phys_port=device.phys)
            card_read_once = False
        else:
            saved_card.phys_port = device.phys
            print(f'posteando a frontend: {saved_card}')
            # requests.post("http://localhost:3000/inform-card-read", json=saved_card.dict())

def start_keyboard_threads():
    keyboards = get_keyboards()
    for keyboard in keyboards:
        thread = threading.Thread(target=watch_keyboard, args=(keyboard,))
        thread.daemon = True
        thread.start()
