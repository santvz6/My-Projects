""" Product entity representation for SQLAlchemy ORM. """

from typing import Optional
from sqlmodel import SQLModel, Field


class Products(SQLModel, table=True):
    """Product model mapped to our database table."""
    
    name: Optional[str] = Field(default=None, primary_key=True)
    description: str
    category_id: int
    price: float
    