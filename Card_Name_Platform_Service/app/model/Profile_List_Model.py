from pydantic import BaseModel, model_validator, Field, ConfigDict
from typing import List, Dict, Any, Optional
from Card_Name_Platform_Service.app.model.Message_Model import *
from typing import Union
from bson import ObjectId


class ShortProfileModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,           # cho phép alias ngược lại khi dump
        extra="allow",
        json_encoders={ObjectId: str}    # chuyển ObjectId thành str khi dump ra JSON                 
    )
    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    name: str = ""
    designation: str = ""
    avatar_location: str = ""
    primary_profile: bool = False

class ProfileListModel(ErrorMessageModel):
    short_profiles: List[ShortProfileModel] = []  