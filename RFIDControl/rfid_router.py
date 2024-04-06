from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from .rfid_control import get_keyboards, get_keyboard_ports, read_card, CardInfo
import threading
import asyncio

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

async def event_stream(request):
    while True:
        if hasattr(request.app.state, 'card_data'):
            yield f"data: {request.app.state.card_data.json()}\n\n"
            delattr(request.app.state, 'card_data')
        await asyncio.sleep(1)

@router.get("/card-read-stream")
async def card_read_stream(request: Request):
    return StreamingResponse(event_stream(request), media_type="text/event-stream")

@router.post("/clear-card-data")
async def clear_card_data():
    global saved_card, card_read_once
    saved_card = None
    card_read_once = False
    return {"message": "Card data cleared"}

def watch_keyboard(device):
    global saved_card, card_read_once
    while True:
        card_number = read_card(device)
        if not saved_card or saved_card.card_number != int(card_number):
            saved_card = CardInfo(card_number=int(card_number), phys_port=device.phys)
            card_read_once = False
        else:
            saved_card.phys_port = device.phys
            asyncio.run(send_sse_event(saved_card))

async def send_sse_event(card_data: CardInfo):
    from main import app
    app.state.card_data = card_data
    print(f'estado de app cambiado a: {card_data}')

def start_keyboard_threads():
    keyboards = get_keyboards()
    for keyboard in keyboards:
        thread = threading.Thread(target=watch_keyboard, args=(keyboard,))
        thread.daemon = True
        thread.start()