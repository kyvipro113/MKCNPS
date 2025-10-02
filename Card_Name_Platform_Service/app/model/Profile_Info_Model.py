from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional


class ProfileInfoBuiltModel(BaseModel):
    designation: str = ""
    bio: str = ""
    area_code: str = ""
    primary_mobile: str = ""
    primary_email: str = ""
    address: str = ""
    #slogan: str = ""
    avatar_name: str = ""
    banner_name: str = ""
    language: str = "vietnamese"
    name: str = ""
    username_link: str = ""