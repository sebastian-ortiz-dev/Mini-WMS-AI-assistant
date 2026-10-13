from pydantic import BaseModel

class AIQueryRequest(BaseModel):
    question: str