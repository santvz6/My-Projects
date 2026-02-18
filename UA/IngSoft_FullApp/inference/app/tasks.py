import os
from celery import Celery
import requests
import base64

from app.models.squeezenet import SqueezeNet

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
BACKEND_WEBHOOK = os.getenv("BACKEND_WEBHOOK", "http://backend:8000/webhook/task_completed")

MODEL_PATH = "app/assets/squeezenet.onnx"
CLASSES_PATH = "app/assets/squeezenet_classes.txt"

celery_app = Celery("inference", broker=REDIS_URL)
celery_app.conf.task_routes = {
    'app.tasks.process_image_task': {'queue': 'image'}
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
)


_model = SqueezeNet(MODEL_PATH, CLASSES_PATH)


############################### IMAGE ###############################
@celery_app.task
def process_image_task(image_b64: str, task_id: str):
    
    state = "completed"
    predictions = []

    try:
        image_data = base64.b64decode(image_b64)
        print(f"[DEBUG] task {task_id}: decoded {len(image_data)} bytes")

        head = image_data[:4].hex()
        tail = image_data[-4:].hex()
        print(f"[DEBUG] task {task_id}: header={head}, footer={tail}")

        predictions = _model(image_data)
        print(f"[PREDICTIONS]: {predictions}")


    except Exception as e:
        state = "failed"
        print(f"[ERROR CELERY task {task_id}]: {e}")

    finally:
        try:
            requests.post(BACKEND_WEBHOOK, json={"task_id": task_id, "state": state, "predictions": predictions})
        except Exception as e:
            print(f"[ERROR webhook post task {task_id}]: {e}")

