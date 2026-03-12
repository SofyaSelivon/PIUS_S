from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

payload = {
    "userId": "9ba4ee01-186e-48a8-a638-a6804d4def84",
    "isSeller": True
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(token)