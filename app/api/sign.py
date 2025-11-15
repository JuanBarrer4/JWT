from fastapi import APIRouter, HTTPException
from core.models import SignRequest
from services.signer_service import sign_token

router = APIRouter(prefix="/sign", tags=["sign"])

@router.post("")
def sign_route(req: SignRequest):
    try:
        header = req.header
        payload = req.payload
        
        alg = req.alg or header.get("alg", "HS256")
        
        if "typ" in header and header["typ"] != "JWT":
            raise ValueError("Header.typ debe ser 'JWT'")
        
    

        return sign_token(header, payload, req.secret, req.alg)
    except Exception as e:
        raise HTTPException(400, str(e))
