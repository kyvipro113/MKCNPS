from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional

from Card_Name_Platform_Service.app.model.Auth_Model import *

class RegisterModel(AuthModel):
    image_name: str = ""
    name: str = ""
    designation: str = ""
    area_code: str = ""
    primary_mobile: str = ""
    primary_email: str = ""
    username_link: str = ""
    language: str = "vietnamese"
