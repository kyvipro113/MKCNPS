from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Message_Model import *

class ObjectPresignedModel(ErrorMessageModel):
    object_name: str = ""
    presigned_link: str = ""


class EmailVerifyCodeModel(BaseModel):
    email: str = ""
    verify_code: str = ""