# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class KnowledgeCreate(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=5)
    tags: Optional[List[str]] = []

class KnowledgeArticle(KnowledgeCreate):
    id: str

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    # backend expects 'customer_name' (matches app.py). Frontend should submit customer_name.
    customer_name: str = Field(..., min_length=2)

class Ticket(TicketCreate):
    id: str
    status: str
    createdAt: str
    recommendedArticleIds: List[str] = []
