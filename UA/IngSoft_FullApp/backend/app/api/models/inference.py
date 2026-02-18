from pydantic import BaseModel, Field


class SearchTextRequest(BaseModel):
    """Text-based search request payload."""
    
    query: str = Field(..., example="camiseta blanca")
