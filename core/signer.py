import hmac, hashlib
from .base64url import b64url_encode

_ALGS = {"HS256": hashlib.sha256, "HS384": hashlib.sha384}

def sign(alg: str, secret: str, signing_input: bytes) -> str:
    if alg not in _ALGS:
        raise ValueError("Algoritmo no soportado")
    mac = hmac.new(secret.encode("utf-8"), signing_input, _ALGS[alg]).digest()
    return b64url_encode(mac)
