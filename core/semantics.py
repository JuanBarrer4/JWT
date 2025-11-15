import json, time
from .base64url import b64url_decode

REQUIRED_HEADER = {"alg", "typ"}

def _json(b64: str) -> dict:
    return json.loads(b64url_decode(b64).decode("utf-8"))

def validate_semantics(h_b64: str, p_b64: str, now: int | None = None) -> dict:
    now = now or int(time.time())
    header = _json(h_b64)
    payload = _json(p_b64)

    missing = [k for k in REQUIRED_HEADER if k not in header]
    if missing: raise ValueError(f"Header incompleto: faltan {missing}")
    if header.get("typ") != "JWT":
        raise ValueError("Header.typ debe ser 'JWT'")
    if header.get("alg") not in {"HS256", "HS384"}:
        raise ValueError("Algoritmo no soportado en este prototipo")

    # Claims temporales.
    for c in ("exp", "nbf", "iat"):
        if c in payload and not isinstance(payload[c], int):
            raise ValueError(f"Claim {c} debe ser entero (epoch)")
    if "exp" in payload and now >= payload["exp"]:
        raise ValueError("Token expirado")

    return {"header": header, "payload": payload}
