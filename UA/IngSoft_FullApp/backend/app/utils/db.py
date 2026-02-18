import logging
from typing import List, Dict
from sqlmodel import select, SQLModel

from app.db.registry import DatabaseRegistry
from app.db.entities import Products, CategoryTypes


logger = logging.getLogger("backend")

# Crea todas las tablas definidas en data/init.sql
SQLModel.metadata.create_all(DatabaseRegistry.get_engine())


def get_all_products() -> List[Products]:
    """
    Devuelve la lista completa de productos almacenados en la base de datos.
    """
    session = DatabaseRegistry.session()
    statement = select(Products)
    results = session.exec(statement)
    return results.all()


def get_products_by_categories(category_names: List[str]) -> List[Products]:
    """
    Devuelve los productos que pertenecen a una o mas categorias especificadas.
    """
    session = DatabaseRegistry.session()

    try:
        # Convertimos los nombres en enums de categoria validos
        category_enums = [CategoryTypes[name.upper()] for name in category_names]
        logger.info(f"{get_products_by_categories.__name__} -> category_enums: {category_enums}")

        # Extraemos los valores numericos asociados a cada categoria
        category_values = [c.value for c in category_enums]
        logger.info(f"{get_products_by_categories.__name__} -> category_values: {category_values}")

    except KeyError:
        # Si alguna categoria no existe devolvemos una lsita vacia
        return []
    
    statement = select(Products).where(Products.category_id.in_(category_values))
    results = session.exec(statement)
    return results.all()


def get_all_categories() -> List[Dict]:
    """
    Obtiene todas las categorias posibles definidas en el Enum 'CategoryTypes'.
    """
    return [{"name": c.name.lower(), "id": c.value} for c in CategoryTypes]