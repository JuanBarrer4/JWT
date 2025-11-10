from .lexer import tokenize_jwt

def parse_jwt_structure(token: str) -> dict:
    toks = tokenize_jwt(token)
    return {"type": "JWT", "children": [{"type": t.type, "value": t.lexeme} for t in toks]}
