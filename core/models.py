from pydantic import BaseModel, Field

class DecodeRequest(BaseModel):
    token: str

class SignRequest(BaseModel):
    header: dict
    payload: dict
    secret: str = Field(min_length=1)
    alg: str = "HS256"

class VerifyRequest(BaseModel):
    token: str
    secret: str
