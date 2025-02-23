from typing import List, Dict, Any, Union
from pydantic import BaseModel
class HotData(BaseModel):
    title: str
    description: str