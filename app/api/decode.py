from fastapi import APIRouter, HTTPException
from core.models import DecodeRequest
from services.decoder_service import decode_token

router = APIRouter(prefix="/decode", tags=["decode"])

@router.post("")
def decode(req: DecodeRequest):
    try:
        return decode_token(req.token)
    except Exception as e:
        raise HTTPException(400, str(e))
