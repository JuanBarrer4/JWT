from fastapi import APIRouter, HTTPException
from core.models import VerifyRequest
from services.verifier_service import verify_token

router = APIRouter(prefix="/verify", tags=["verify"])

@router.post("")
async def verify(req: VerifyRequest):
    try:
        return await verify_token(req.token, req.secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
