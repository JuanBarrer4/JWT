from fastapi import APIRouter, HTTPException
from core.models import DecodeRequest
from services.validator_service import validate_token

router = APIRouter(prefix="/validate", tags=["validate"])

@router.post("")
def validate(req: DecodeRequest):
    try:
        return validate_token(req.token)
    except Exception as e:
        raise HTTPException(400, str(e))
