"""
Weeebhook API for receiving task completion notifications from the inference server.
This API is used to receive the results of tasks that have been processed by the inference server.
The inference server sends a POST request to this API with the task ID and the result of the task.

You can learn more about the webhook API in the following link:
https://fastapi.tiangolo.com/advanced/openapi-webhooks/
"""
from fastapi import APIRouter, status
from typing import Dict

from .models import TaskResult


router = APIRouter()


@router.post(
    "/webhook/task_completed",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Recibir notificación de tarea completada",
    description="Recibe notificaciones del servidor de inferencia una vez que una tarea ha sido completada. "
                "El cuerpo de la solicitud debe contener el 'task_id', el 'state' y la 'prediccion'.",
    tags=["webhook"]
)
async def receive_task_result(payload: TaskResult) -> Dict[str, str]:
    from app.state import result_store

    if payload.state == "completed":
        result_store[payload.task_id] = payload.predictions
    else:
        result_store[payload.task_id] = "failed"

    return {"status": "received"}
