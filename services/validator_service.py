from core.parser import parse_jwt_structure
from core.semantics import validate_semantics

def validate_token(jwt: str) -> dict:
    parts = jwt.split(".")
    ast = parse_jwt_structure(jwt)
    sem = validate_semantics(parts[0], parts[1])
    return {"ast": ast, "semantics": sem}
