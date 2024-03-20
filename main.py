import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["127.0.0.1:3000", "localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getPassword/{fuente}")
async def fetch_api_key_caja(fuente: str):
    api_key = None
    
    if fuente == 'caja':
        api_key = os.getenv("API_KEY_TERMINAL_CAJA")
    elif fuente == 'tapa':
        api_key = os.getenv("API_KEY_TERMINAL_TAPA")
    elif fuente == 'admin':
        api_key = os.getenv("API_KEY_TERMINAL_ADMIN")
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"api_key": api_key}

if __name__ == '__main__':
    uvicorn.run("backend_gestor_credenciales:app", port=3001, reload=True)