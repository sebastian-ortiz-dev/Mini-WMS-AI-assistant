from pydantic import BaseModel, Field

class InventoryReceiveRequest(BaseModel):
    sku: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="product SKU",
        examples=["SKU-PAINT-001"]
    )
    bin_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,  
        description="ID bin/localition",
        examples=["UUID"]
    )
    movement: str = Field(
            ..., 
            min_length=1, 
            max_length=100,  
            description="ID movement"
        )
    quantity: int = Field(
        ..., 
        gt=0, 
        description="quantity (must be more than 0)",
        examples=[50]
    )

class InventoryExchangeRequest(BaseModel):
    sku: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="product SKU",
        examples=["SKU-PAINT-001"]
    )
    from_bin_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,  
        description="ID bin/localition",
        examples=["UUID"]
    )
    to_bin_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,  
        description="ID bin/localition",
        examples=["UUID"]
    )
    movement: str = Field(
            ..., 
            min_length=1, 
            max_length=100,  
            description="ID movement"
        )
    quantity: int = Field(
        ..., 
        gt=0, 
        description="quantity (must be more than 0)",
        examples=[50]
    )

class MovementsResponse(BaseModel):
    id_external: str | None = Field(
      None
    )
    movement: str | None = Field(
      None
     )

class InventoryReceiveResponse(BaseModel):
    message: str
    movement: str