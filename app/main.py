from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import conversation
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv
import os

from app.database import init_db

load_dotenv()

app = FastAPI(title="Personalized Networking Assistant")

@app.on_event("startup")
def on_startup():
    init_db()

# API Key configuration
API_KEY = os.getenv("API_KEY", "my_super_secret_api_key_123") 
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Ye function har request par API Key check karega
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key! Access Denied."
    )

# CORS Middleware Setup (Frontend ko connect karne dene ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" ka matlab hai kisi bhi frontend se request aa sakti hai
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET sab methods allow karega
    allow_headers=["*"],
)

app.include_router(conversation.router, dependencies=[Depends(get_api_key)])

@app.get("/")
def root():
    return {"message": "Welcome!"}
