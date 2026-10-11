from pydantic import BaseModel
from typing import List

class JDRequest(BaseModel):
    title: str
    experience: str
    skills: List[str]
    description: str