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

@app.get("/getPassword")
async def fetch_api_key_caja():
    api_key_names = [
        'API_KEY_TERMINAL_CAJA',
        'API_KEY_TERMINAL_TAPA',
        'API_KEY_TERMINAL_ADMIN',
    ]
    api_key = None
    
    for key_name in api_key_names:
        api_key = os.getenv(key_name)
        if api_key: break

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"api_key": api_key}

# @app.get("/getPassword/{fuente}")
# async def fetch_api_key_caja(fuente: str):
#     api_key = None
    
#     if fuente == 'caja':
#         api_key = os.getenv("API_KEY_TERMINAL_CAJA")
#     elif fuente == 'tapa':
#         api_key = os.getenv("API_KEY_TERMINAL_TAPA")
#     elif fuente == 'admin':
#         api_key = os.getenv("API_KEY_TERMINAL_ADMIN")
    
#     if not api_key:
#         raise HTTPException(status_code=404, detail="API key not found")
    
#     return {"api_key": api_key}

if __name__ == '__main__':
    puerto = os.getenv('PORT', 3001)
    uvicorn.run("main:app", port=int(puerto), reload=True)