from fastapi import APIRouter
from typing import List, Dict, Any

from app.utils import get_all_products, get_all_categories

router = APIRouter()

@router.get(
    "/products",
    summary="Listar todos los productos",
    description="Obtiene una lista completa de productos disponibles, incluyendo su nombre, descripción, ID de categoría y precio.",
    tags=["products"]
)
def list_products() -> Dict[str, List[Dict[str, Any]]]:
    products = get_all_products()
    return {
        "products": [
            {
                "name": p.name,
                "description": p.description,
                "category_id": p.category_id,
                "price": p.price
            }
            for p in products
        ]
    }

@router.get(
    "/categories",
    summary="Listar todas las categorías",
    description="Devuelve un listado de todas las categorías disponibles para clasificar productos.",
    tags=["categories"]
)
async def categories() -> List[Dict[str, Any]]:
    return get_all_categories()
