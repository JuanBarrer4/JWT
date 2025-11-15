from core.parser import parse_jwt_structure
from core.semantics import _json, validate_semantics
from core.database import get_database
import hmac, hashlib, base64

async def verify_token(jwt: str, secret_key: str):
    db = get_database()

    try:
        # 1️. Separar las tres partes
        parts = jwt.split(".")
        if len(parts) != 3:
            raise ValueError("El token debe tener 3 partes (header, payload y firma)")
        h_b64, p_b64, s_b64 = parts

        # 2️. Decodificar header y payload
        header = _json(h_b64)
        payload = _json(p_b64)

        # 3️. Seleccionar algoritmo
        alg = header.get("alg", "HS256")
        if alg not in {"HS256", "HS384"}:
            raise ValueError(f"Algoritmo no soportado: {alg}")

        hash_func = hashlib.sha256 if alg == "HS256" else hashlib.sha384

        # 4️. Recalcular firma esperada
        signing_input = f"{h_b64}.{p_b64}".encode()
        expected_signature = hmac.new(secret_key.encode(), signing_input, hash_func).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip("=")

        # 5️. Normalizar ambas firmas (quitar padding "=")
        s_b64_clean = s_b64.rstrip("=")
        valid_signature = (expected_sig_b64 == s_b64_clean)

        
        #print("Esperada:", expected_sig_b64)
        #print("Proporcionada:", s_b64_clean)

        # 6️. Validar semántica si la firma es válida
        semantics = None
        if valid_signature:
            semantics = validate_semantics(h_b64, p_b64)

        # 7️. Resultado DB.
        result = {
            "jwt": jwt,
            "status": "válido" if valid_signature else "no válido",
            "semantics": semantics,
            "signature": {
                "algorithm": alg,
                "valid": valid_signature,
                "provided_signature_b64": s_b64,
                "expected_signature_b64": expected_sig_b64
            }
        }

        # 8️. Guardar en la base de datos
        inserted_doc = None
        if db is not None:
            insert_result = await db.validation_results.insert_one(result)
            inserted_doc = await db.validation_results.find_one({"_id": insert_result.inserted_id})

        if not valid_signature:
            raise ValueError("Firma no válida: no coincide con la esperada")

        # Convertir ObjectId a string
        if inserted_doc and "_id" in inserted_doc:
            inserted_doc["_id"] = str(inserted_doc["_id"])
            return inserted_doc

        return result

    except Exception as e:
        if db is not None:
            await db.validation_results.insert_one({
                "jwt": jwt,
                "status": "no válido",
                "error": str(e)
            })
        raise
