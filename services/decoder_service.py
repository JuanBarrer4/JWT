from core.parser import parse_jwt_structure
from core.semantics import _json

def decode_token(jwt: str) -> dict:
    ast = parse_jwt_structure(jwt)
    h_b64, p_b64 = jwt.split(".")[0:2]
    return {"ast": ast, "header": _json(h_b64), "payload": _json(p_b64)}
