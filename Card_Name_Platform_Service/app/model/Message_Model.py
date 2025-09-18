from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional

class ErrorMessageModel(BaseModel):
    message: str = ""