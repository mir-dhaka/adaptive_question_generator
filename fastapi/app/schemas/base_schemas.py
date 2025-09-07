from pydantic import BaseModel
from typing import List, Optional

class BaseResponse(BaseModel):
    success: bool
    message:str 
    errorList:dict
    isList:bool
    data:object 
