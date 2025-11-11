from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from contextlib import asynccontextmanager

# URI de conexión al cluster de MongoDB Atlas
MONGO_URI = "mongodb+srv://information:DAElxC1ePXGkfNTx@cluster0.kirnqlk.mongodb.net/"

# Nombre de la base de datos
DATABASE_NAME = "JWT_Analyzer"

# Variables globales
client: AsyncIOMotorClient = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    print("Conectado con MongoDB")
    yield  # Aquí corre la aplicación mientras está activa
    client.close()
    print("Conexión con MongoDB cerrada")


# Devuelve la base de datos para usar en los endpoints
def get_database():
    return db


# Inicializa la app con el lifespan integrado
def create_app():
    app = FastAPI(title="JWT Analyzer LF 2025-2 (local)", lifespan=lifespan)
    return app