from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional
from Generative_AI_Service.app.model.Message_Model import *


class TokenModel(BaseModel):
    access_token: str = ""
    refresh_token: str = ""
    expires: int = -1

class ThirdPartyTokenModelRtn(ErrorMessageModel):
    data: Optional[TokenModel] = None

    

