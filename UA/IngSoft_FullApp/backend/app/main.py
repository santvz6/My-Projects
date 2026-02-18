import os
import logging
from fastapi import FastAPI

from app.api import products, inference, webhook


# Configuración del Backend Logger
os.makedirs("/app/logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    filename="/app/logs/backend.log",
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("backend")


# Crea la app FastAPI
app = FastAPI(title="E-commerce Search API")


############################### ENDPOINTS ###############################
@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(inference.router)
app.include_router(products.router)
app.include_router(webhook.router)
