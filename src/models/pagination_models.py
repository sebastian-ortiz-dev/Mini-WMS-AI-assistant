from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class StockMovementItemResponse(BaseModel):
    id_external: str = Field(..., description="External UUID of the movement")
    username: str = Field(..., description="User who performed the action")
    movement: str = Field(..., description="Type of movement (Reception, Transfer, Pick, etc.)")
    quantity: int = Field(..., description="Quantity involved")
    item_name: str = Field(..., description="Name of the item")
    sku: str = Field(..., description="Item SKU")
    from_bin_code: Optional[str] = Field(None, description="Source bin code (if applicable)")
    to_bin_code: Optional[str] = Field(None, description="Destination bin code (if applicable)")
    created_at: datetime = Field(..., description="Timestamp when the movement was created")

    class Config:
        from_attributes = True

class PaginatedStockMovementsResponse(BaseModel):
    total_pages: int = Field(..., description="Total number of calculated pages")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    data: List[StockMovementItemResponse] = Field(..., description="List of stock movements")


class StockPerBinItemResponse(BaseModel):
    sku: str = Field(..., description="Item SKU")
    name: str = Field(..., description="Name of the item")
    image: Optional[str] = Field(None, description="Image filename or URL of the item")
    bin_code: str = Field(..., description="Generated code of the bin/location")
    quantity_available: int = Field(..., description="Quantity currently available in this bin")
    quantity_reserved: int = Field(..., description="Quantity reserved for pending orders in this bin")

    class Config:
        from_attributes = True

class PaginatedStockPerBinResponse(BaseModel):
    total_pages: int = Field(..., description="Total number of calculated pages")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    data: List[StockPerBinItemResponse] = Field(..., description="List of stock records per bin")