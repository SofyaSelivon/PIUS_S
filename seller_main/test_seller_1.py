# test_seller_1.py
from fastapi.testclient import TestClient
from app.main import app  # импортируй твой FastAPI instance
from app.security.jwt_dependency import SECRET_KEY, ALGORITHM
from jose import jwt
from uuid import uuid4

# Создаем фиктивный токен для теста
TEST_USER_ID = uuid4()  # случайный UUID
token_payload = {"userId": str(TEST_USER_ID), "isSeller": True}
test_token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

client = TestClient(app)

def run_tests():
    headers = {"Authorization": f"Bearer {test_token}"}

    print("=== GET /api/markets/my ===")
    response = client.get("/api/markets/my", headers=headers)
    print(response.status_code, response.json())

    print("=== PATCH /api/markets/my ===")
    response = client.patch(
        "/api/markets/my",
        headers=headers,
        json={"marketName": "Test Store", "description": "Test description"}
    )
    print(response.status_code, response.json())

    print("=== GET /api/products/my ===")
    response = client.get("/api/products/my?page=1&limit=5", headers=headers)
    print(response.status_code, response.json())

    print("=== POST /api/products/ ===")
    response = client.post(
        "/api/products/",
        headers=headers,
        json={
            "name": "Test Product",
            "description": "Test product desc",
            "category": "electronics",
            "price": 99.99,
            "available": 10,
            "img": "test.png"
        }
    )
    print(response.status_code, response.json())

if __name__ == "__main__":
    run_tests()