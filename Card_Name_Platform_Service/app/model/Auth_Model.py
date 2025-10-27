from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional

class AuthModel(BaseModel):
    email: str
    password: str

    @model_validator(mode="after")
    def check_empty(cls, values):
        if not values.email or not values.password:
            raise ValueError("Email and password must be provided")
        return values
    
class AuthModelWithCard(AuthModel):
    card_id: str = ""
    pin: str = ""