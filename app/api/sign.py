from fastapi import APIRouter, HTTPException
from core.models import SignRequest
from services.signer_service import sign_token

router = APIRouter(prefix="/sign", tags=["sign"])

@router.post("")
def sign_route(req: SignRequest):
    try:
        return sign_token(req.header, req.payload, req.secret, req.alg)
    except Exception as e:
        raise HTTPException(400, str(e))
