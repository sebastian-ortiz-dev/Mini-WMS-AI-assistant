from pydantic import BaseModel, Field
from typing import Optional

class BinCreate(BaseModel):
    aisle: int = Field(..., description="aisle number", examples=[1, 2])
    bay: str = Field(
        ..., max_length=10, description="code of bay", examples=["A"]
    )
    tier: int = Field(..., description="tier", examples=[1, 2])
    position: str = Field(
        ..., max_length=10, description="Position", examples=["01"]
    )

class BinUpdateSchema(BaseModel):
    aisle: Optional[int] = Field(None, description="aisle number")
    bay: Optional[str] = Field(None, max_length=10, description="code of bay")
    tier: Optional[int] = Field(None, description="tier")
    position: Optional[str] = Field(None, max_length=10, description="Position")

class ListBins(BaseModel):
    id_external: str
    generated_code: str
