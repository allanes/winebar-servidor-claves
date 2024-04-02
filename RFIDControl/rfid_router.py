from fastapi import APIRouter, HTTPException
from .rfid_control import get_keyboard_ports, get_saved_phys_port

router = APIRouter()

@router.get("/keyboard_ports")
def keyboard_ports():
    ports = get_keyboard_ports()
    return {"keyboard_ports": ports}

@router.post("/get_phys_port")
def phys_port(card_number: int):
    phys_port = get_saved_phys_port(card_number)
    if phys_port:
        return {"phys_port": phys_port}
    else:
        raise HTTPException(status_code=404, detail="Card data not found")