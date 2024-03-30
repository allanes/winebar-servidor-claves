from fastapi import APIRouter, HTTPException
from .raspi_config import lcd
from .funciones_lcd import print_info_cliente, InfoCliente, limpiar_pantalla

router = APIRouter()

@router.post("/clear")
async def handle_clear_display():
    limpiar_pantalla(lcd)

@router.post("/")
async def display_info_cliente(info: InfoCliente):
    try:
        print_info_cliente(lcd, info)
        return {"message": "Info displayed on LCD successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
