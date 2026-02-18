from pydantic import BaseModel, Field
from typing import List


class Prediction(BaseModel):
    """Inference result for a single task."""

    label: str = Field(..., example="T-shirt")
    score: float = Field(..., ge=0, le=1, example=0.97)


class TaskResult(BaseModel):
    """Task result received from the inference server."""

    task_id: str = Field(..., example="f6a24199-b3b3-4bf2-87eb-de7973fbfa99")
    state: str = Field(..., example="completed")
    predictions: List[Prediction]