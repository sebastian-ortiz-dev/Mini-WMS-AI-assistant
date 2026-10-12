from pydantic import BaseModel, Field
from datetime import datetime

# --- ESQUEMAS PARA LA CREACIÓN DE ÓRDENES ---

class OrderItemCreate(BaseModel):
    item_sku: str = Field(..., description="Product sku")
    bin_id_external: str = Field(..., description="Bin ID")
    quantity: int = Field(..., gt=0, description="Amount requested")

class OrderCreateSchema(BaseModel):
    items: list[OrderItemCreate] = Field(..., description="List of items")


class OrderResponseSchema(BaseModel):
    id_external: str
    created_at: datetime

class OrderResponsePick(BaseModel):
    id_external: str
    picked_at: datetime

class OrderResponseShip(BaseModel):
    id_external: str
    shipped_at: datetime