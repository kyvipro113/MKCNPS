from pydantic import BaseModel, model_validator, Field, field_validator, ConfigDict
from typing import List, Dict, Any, Optional, Union
from bson import ObjectId

class Widget_Company_Branch(BaseModel):
    branch_name: str = ""
    area_code: str = ""
    phone: str = ""
    address_list: List[str] = []
    

class Widget_Company(BaseModel):
    company_name: str = ""
    company_logo: str = ""
    company_email: str = ""
    company_website: str = ""
    branch_list: List[Widget_Company_Branch] = []
    layout_position: int = -1
    
class Widget_Custom_Link(BaseModel):
    link_name: str = ""
    link_address: str = ""
    layout_position: int = -1

class Widget_Email(BaseModel):
    email: str = ""
    layout_position: int = -1

class Widget_Image_Gallery(BaseModel):
    image_locations: List[str] = []
    layout_position: int = -1

class Widget_Mobile(BaseModel):
    mobile_number: str = ""
    layout_position: int = -1

class Widget_Social_Network_Link(BaseModel):
    social_network_name: str = ""
    social_network_link: str = ""
    layout_position: int = -1
    
    
class Group_Branch(BaseModel):
    area_code: str = ""
    phone: str = ""
    address: List[str] = []

class Group_Info_Rtn(BaseModel):
    # group_id: str = ""
    group_name: str = ""
    group_logo: str = ""
    group_email: str = ""
    group_website: str = ""
    branch_list: List[Group_Branch] = []
    accents_color: str = "#ffffff"
    background_color: str = "#000000"
    language: str = "vietnamese"
    theme_type: str = "00"
    primary_group: bool = False

class Group_Info(Group_Info_Rtn):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,           # cho phép alias ngược lại khi dump
        json_encoders={ObjectId: str} 
    )

    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    