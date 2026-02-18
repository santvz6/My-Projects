import uuid
import os
import logging

from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from app.tasks import process_image_task


os.makedirs("/app/logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    filename="/app/logs/inference.log",
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("inference")


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}


class InferRequest(BaseModel):
    image_b64: str
    task_id: str

@app.post("/infer/image")
async def infer_image(req: InferRequest):
    logger.info(f"Inference: recibiendo tarea {req.task_id}")
    process_image_task.delay(req.image_b64, req.task_id)
    return {"task_id": req.task_id}