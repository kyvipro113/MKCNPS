from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional
from Card_Name_Platform_Service.app.model.Message_Model import *

class ShortProfileModel(BaseModel):
    profile_id: str = ""
    name: str = ""
    avatar_url: str = ""
    is_primary: bool = False

class ProfileListModel(ErrorMessageModel):
    short_profiles: List[ShortProfileModel] = []  