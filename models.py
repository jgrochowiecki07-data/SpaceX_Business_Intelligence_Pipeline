from pydantic import BaseModel, Field
from typing import Optional

class LaunchData(BaseModel):
    name: str
    details: Optional[str]
    success: Optional[bool]
    sentiment_score: float = Field(ge=-1.0, le=1.0)