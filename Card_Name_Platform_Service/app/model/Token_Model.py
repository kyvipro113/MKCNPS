from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional, Union
from Card_Name_Platform_Service.app.model.Message_Model import *
# from Generative_AI_Service.app.model.Message_Model import *

class PayloadEndUserModel(BaseModel):
    uid: str = ""
    flag: bool = False
    #change_profile: bool = False
    token_type: str = ""
    email: str = ""
    role: str = "user"
    model_config = {"extra": "allow"}  # Extending to allow additional fields (exp, token_type, email, ....)

class PayloadManagerModel(BaseModel):
    uid: str = ""
    group_id: str = ""
    username: str = ""
    name: str = ""
    status: str = ""
    token_type: str = ""
    role: str = "manager"
    model_config = {"extra": "allow"}  # # Extending to allow additional fields (exp, token_type)

class TokenPayloadModel(BaseModel):
    token: str = ""
    payload: Union[PayloadEndUserModel, PayloadManagerModel] = {}

class TokenModel(ErrorMessageModel):
    access_token: str = ""
    refresh_token: str = ""
    # flag: bool = False
    # change_profile: bool = False

# class ManagerTokenModel(ErrorMessageModel):
#     access_token: str = ""
#     refresh_token: str = ""
    

# class ThirdPartyTokenModelRtn(ErrorMessageModel):
#     data: Optional[TokenModel] = None

# class TokenModelRtn(ErrorMessageModel):
#     access_token: str = ""
#     refresh_token: str = ""
#     flag: str = ""

