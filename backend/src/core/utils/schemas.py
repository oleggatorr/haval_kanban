# src\core\utils\schemas.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any

class BaseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseResponce(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class IdRequest():
    pass

class ArrayRequest():
    pass



class ArrayResponce(BaseModel):
    """"""
    total: int = 0
    data: Optional[Any] = None

