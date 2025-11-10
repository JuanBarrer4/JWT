from dataclasses import dataclass

@dataclass
class Token:
    type: str
    lexeme: str

def tokenize_jwt(token: str) -> list[Token]:
    parts = token.split(".")
    if len(parts) not in (2, 3):
        raise ValueError("JWT mal formado: se esperan 2 o 3 partes separadas por '.'")
    types = ["HEADER_B64", "PAYLOAD_B64"] + (["SIGNATURE_B64"] if len(parts) == 3 else [])
    return [Token(t, p) for t, p in zip(types, parts)]
