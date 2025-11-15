import json
from core.base64url import b64url_encode
from core.signer import sign

def sign_token(header: dict, payload: dict, secret: str, alg: str = "HS256") -> dict:
    
    h = b64url_encode(json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    p = b64url_encode(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    
    signing_input = f"{h}.{p}".encode("ascii")
    sig = sign(alg, secret, signing_input)
    return {"token": f"{h}.{p}.{sig}"}
