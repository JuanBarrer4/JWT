from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import decode, validate, sign
from .api import verify

app = FastAPI(title="JWT Analyzer LF 2025-2 (local)")

# Angular dev server corre por defecto en http://localhost:4200
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(decode.router)
app.include_router(validate.router)
app.include_router(sign.router)
app.include_router(verify.router)
