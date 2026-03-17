from fastapi import FastAPI
from app.routes.market_routes import router as market_router
from app.routes.product_routes import router as product_router
from fastapi.middleware.cors import CORSMiddleware
import app.models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router)
app.include_router(product_router)