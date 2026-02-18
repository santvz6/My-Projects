import logging
import requests, base64, uuid

from fastapi import APIRouter, UploadFile, File

from .models import SearchTextRequest
from app.utils import search_categories_from_text, get_products_by_categories
from app.state import result_store


logger = logging.getLogger("backend")
router = APIRouter()


INFERENCE_API_URL = "http://inference_api:9000"  


############################### TEXT ENDPOINTS ###############################
@router.post(
    "/search/text",
    status_code=200,
    summary="Buscar productos a partir de una consulta de texto",
    description="Recibe una cadena de texto como consulta, predice las categorías asociadas usando (NLP)," \
    " y devuelve los productos relacionados con dichas categorías.",
    tags=["search"]
)
async def search_text(text_request: SearchTextRequest) -> dict:

    # Uso __name__ en caso de hacer refactorización (cambiarle el nombre a la función)
    logger.info(f"{search_text.__name__} -> query: {text_request.query}")

    categories = search_categories_from_text(text_request.query)
    logger.info(f"{search_text.__name__} -> categories: {categories}")

    products = get_products_by_categories(categories)
    logger.info(f"{search_text.__name__} -> products: {products}")

    # Pasamos de List[Product] a una Lista serializable a JSON
    products_serialized = [product.model_dump() for product in products] 

    return {"categories": categories, "products": products_serialized}


############################### IMAGE ENDPOINTS ###############################
@router.post(
    "/search/image/",
    status_code=200,
    summary="Buscar productos a partir de una imagen",
    description="Recibe una imagen y la envía al modelo de inferencia para predecir categorías relacionadas. " \
    "Devuelve un 'task_id' que puede usarse para consultar los resultados posteriormente.",
    tags=["search"]
)
async def search_image(file: UploadFile = File(...)) -> dict:
    
    task_id = str(uuid.uuid4())
    image_bytes = await file.read()

    # Codificamos en b64 para Celery
    image_b64 = base64.b64encode(image_bytes).decode("utf-8") 
    
    resp = requests.post(f"{INFERENCE_API_URL}/infer/image", json= {"image_b64": image_b64, "task_id": task_id})
    resp.raise_for_status()

    return {"task_id": task_id}


############################### TASKS ENDPOINTS ###############################
@router.get(
    "/tasks/{task_id}/result",
    status_code=200,
    summary="Obtener resultados de una tarea de inferencia por imagen",
    description="Dado un 'task_id', devuelve el estado de la tarea ('pending', 'testing', 'failed', 'completed') y, si está completada, " \
    "también las categorías inferidas y los productos asociados. Se puede ajustar un umbral para filtrar predicciones poco confiables.",
    tags=["tasks"]
)
async def task_status(task_id: str, threshold: float = 0.1) -> dict:

    predictions = result_store.get(task_id, None)

    # predictions: Dict[str, List[Prediction]] | str
    # Dict --> completed (hay task_id con predicción)
    # str --> failed or testing
    # None --> pending (no hay task_id todavía)
    
    if predictions == "failed":
        return {"status": "failed", "categories": [], "products": []}

    if predictions == "testing":
        return {"status": "testing", "categories": [], "products": []}

    if predictions is None:
        return {"status": "pending", "categories": [], "products": []}


    if not (0 <= threshold <= 1):
        threshold = 0.1
        logger.info(f"{task_status.__name__} -> Exception: threshold inválido")

    # Filtramos Predicciones que superan el Umbral (threshold)
    filtered_predictions = list()
    for prediction in predictions:
        if prediction.score > threshold:
            filtered_predictions.append(prediction)
    
    # Obtenemos las multiples categorias
    categories_array = list()
    for prediction in filtered_predictions:
        categories_array.append(search_categories_from_text(prediction.label))
    
    # Eliminamos categorias duplicadas y aplanamos el Array 2D
    categories = set(cat for sublist in categories_array for cat in sublist)
    categories = list(categories)
    logger.info(f"{task_status.__name__} -> categories: {categories}")

    products = get_products_by_categories(categories)
    logger.info(f"{task_status.__name__} -> products: {products}")

    return {"status": "completed", "categories": categories, "products": products}
