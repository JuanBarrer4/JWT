import jwt

payload = {"sub": "123456", "name": "Alisson Páez", "admin": True}
secret = "mipassword"
token = jwt.encode(payload, secret, algorithm="HS256")

print("Token generado:\n", token)
