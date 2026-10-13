from pydantic import BaseModel, Field
from typing import Optional

class UserResponseSchema(BaseModel):
    id_external: str = Field(..., description="Id external user")
    username: str = Field(..., description="user name")
    image: Optional[str] = Field(None, description="image")