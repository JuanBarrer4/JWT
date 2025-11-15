from core.parser import parse_jwt_structure
from core.semantics import validate_semantics
from core.database import get_database

async def validate_token(jwt: str) -> dict:
    
    db = get_database()

    try:
        # 1️ Separar el token en sus partes
        parts = jwt.split(".")
        if len(parts) < 2:
            if db:
                await db.validation_results.insert_one({
                    "jwt": jwt,
                    "status": "no válido",
                    "error": "El token no tiene las partes necesarias (header y payload)."
                })
            raise ValueError("El token no tiene las partes necesarias (header y payload).")

        # 2️ Analizar estructura
        ast = parse_jwt_structure(jwt)

        # 3️ Validar semántica
        sem = validate_semantics(parts[0], parts[1])

        # 4️ Resultado DB
        result = {
            "jwt": jwt,
            "status": "válido",
            "ast": ast,
            "semantics": sem
        }

        if db is not None:
            await db.validation_results.insert_one(result)

        return result

    except Exception as e:
        # Si algo falla, se guarda también en la base de datos
        if db is not None:
            await db.validation_results.insert_one({
                "jwt": jwt,
                "status": "no válido",
                "error": str(e)
            })
        raise
