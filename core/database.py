from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from contextlib import asynccontextmanager

# URI de conexión al cluster de MongoDB Atlas
MONGO_URI = "mongodb+srv://alissonpaez_db_user:YmtuUGE8Ye0hw5Mj@cluster0.qdjnp84.mongodb.net/?appName=Cluster0"

# Nombre de la base de datos
DATABASE_NAME = "JWT_Analyzer_DB"


client: AsyncIOMotorClient = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    print("Conectado con MongoDB")
    yield  
    client.close()
    print("Conexión con MongoDB cerrada")


# Devuelve la base de datos para usar en los endpoints
def get_database():
    return db


# lifespan para inicializar la app.
def create_app():
    app = FastAPI(title="JWT Analyzer LF 2025-2 (local)", lifespan=lifespan)
    return app