from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    item_sku: str = Field(..., description="Product sku")
    bin_id_external: str = Field(..., description="Bin ID")
    quantity: int = Field(..., gt=0, description="Amount requested")

class OrderCreateSchema(BaseModel):
    items: list[OrderItemCreate] = Field(..., description="List of items")

class OrderListItemSchema(BaseModel):
    id_external: str = Field(..., description="External UUID of the order")
    username: str = Field(..., description="User who created the order")
    status: str = Field(..., description="Current status name of the order")
    created_at: datetime = Field(..., description="Timestamp when the order was created")

class OrderItemDetailSchema(BaseModel):
    sku: str = Field(..., description="Item SKU")
    name: str = Field(..., description="Item name")
    bin_code: str = Field(..., description="Bin code where the item is located/requested from")
    quantity_requested: int = Field(..., description="Quantity requested for this item")
  
class PaginatedOrdersResponse(BaseModel):
    total_pages: int = Field(..., description="Total number of calculated pages")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    data: List[OrderListItemSchema] = Field(..., description="List of orders")

class OrderDetailResponseSchema(BaseModel):
    id_external: str = Field(..., description="External UUID of the order")
    username: str = Field(..., description="User who created the order")
    status: str = Field(..., description="Current status name of the order")
    created_at: datetime = Field(..., description="Timestamp when the order was created")
    items: List[OrderItemDetailSchema] = Field(..., description="List of items included in the order")

class OrderStatusHistoryItemSchema(BaseModel):
    id_external: str = Field(..., description="External UUID of the status history event")
    username: str = Field(..., description="User who triggered the status change")
    sku: str = Field(..., description="Item SKU")
    item_name: str = Field(..., description="Item name")
    quantity_requested: int = Field(..., description="Quantity requested")
    status: str = Field(..., description="Order status at this point")
    changed_at: datetime = Field(..., description="Timestamp when the status changed")
    bin_code: str = Field(..., description="Bin code associated with the item")

class PaginatedOrderStatusHistoryResponse(BaseModel):
    total_pages: int = Field(..., description="Total number of pages available")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page limit")
    data: List[OrderStatusHistoryItemSchema] = Field(..., description="List of history events")


class OrderResponseSchema(BaseModel):
    id_external: str
    created_at: datetime

class OrderResponsePick(BaseModel):
    id_external: str
    picked_at: datetime

class OrderResponseShip(BaseModel):
    id_external: str
    shipped_at: datetime
