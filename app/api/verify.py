from fastapi import APIRouter, HTTPException
from core.models import VerifyRequest
from services.verifier_service import verify_token

router = APIRouter(prefix="/verify", tags=["verify"])

@router.post("")
def verify(req: VerifyRequest):
    try:
        return verify_token(req.token, req.secret)
    except Exception as e:
        raise HTTPException(400, str(e))
