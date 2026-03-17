from fastapi import FastAPI
from app.routes import seller_orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="[SELLER] Order List")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(seller_orders.router)