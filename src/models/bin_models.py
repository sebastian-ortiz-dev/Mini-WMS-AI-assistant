from pydantic import BaseModel, Field


class BinCreate(BaseModel):
    aisle: int = Field(..., description="aisle number", examples=[1, 2])
    bay: str = Field(
        ..., max_length=10, description="Id of bay", examples=["A"]
    )
    tier: int = Field(..., description="tier", examples=[1, 2])
    position: str = Field(
        ..., max_length=10, description="Position", examples=["01"]
    )
    generated_code: str | None = Field(None,max_length=50,description=( "Códe format (ej. 1-A-1-01). it is autogenerator or it can be type."),
       )

class ListBins(BaseModel):
    id_external: str
    generated_code: str
