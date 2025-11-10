from core.signer import sign
from core.semantics import validate_semantics

def verify_token(token: str, secret: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("JWT debe tener 3 partes para verificar firma")
    h_b64, p_b64, s_b64 = parts

    # 1) Validación semántica (alg, typ, claims/tiempos)
    sem = validate_semantics(h_b64, p_b64)

    # 2) Verificación criptográfica
    header = sem["header"]
    alg = header.get("alg")
    signing_input = f"{h_b64}.{p_b64}".encode("ascii")
    expected_sig_b64 = sign(alg, secret, signing_input)

    valid_signature = (expected_sig_b64 == s_b64)

    return {
        "semantics": sem,
        "signature": {
            "algorithm": alg,
            "valid": valid_signature,
            "provided_signature_b64": s_b64,
            "expected_signature_b64": expected_sig_b64
        }
    }
