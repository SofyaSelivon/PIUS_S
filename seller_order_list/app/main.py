from fastapi import FastAPI
from app.routes import seller_orders

app = FastAPI(title="[SELLER] Order List")

# Роуты
app.include_router(seller_orders.router)