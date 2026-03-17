from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

payload = {
    "userId": "42ff4927-d9ed-45d3-91ca-27c0c2220f0f",
    "isSeller": True
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(token)