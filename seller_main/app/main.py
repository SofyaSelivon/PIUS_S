from fastapi import FastAPI
from app.routes.market_routes import router as market_router
from app.routes.product_routes import router as product_router

app = FastAPI()

app.include_router(market_router)
app.include_router(product_router)