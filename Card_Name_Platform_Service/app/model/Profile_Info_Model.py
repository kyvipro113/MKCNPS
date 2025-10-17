from pydantic import BaseModel, model_validator, Field, field_validator, ConfigDict
from typing import List, Dict, Any, Optional, Union
from bson import ObjectId
from Card_Name_Platform_Service.app.model.Widget_Model import *
from Card_Name_Platform_Service.app.model.Message_Model import *

class ProfileInfoBuiltModel(BaseModel):
    designation: str = ""
    bio: str = ""
    area_code: str = ""
    primary_mobile: str = ""
    primary_email: str = ""
    address: str = ""
    #slogan: str = ""
    avatar_name: Optional[Union[str|None]] = None
    banner_name: Optional[Union[str|None]] = None
    language: str = "vietnamese"
    name: str = ""
    username_link: str = ""

class ProfileInfoModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,           # cho phép alias ngược lại khi dump
        extra="allow",
        json_encoders={ObjectId: str}    # chuyển ObjectId thành str khi dump ra JSON                
    )

    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    account_mode: str = "free user"
    change_profile: bool = True
    name: str = ""
    designation: str = ""
    bio: str = ""
    area_code: str = ""
    primary_mobile: str = ""
    primary_email: str = ""
    address: str = ""
    slogan: str = ""
    avatar_location: Optional[Union[str|None]] = None
    banner_location: Optional[Union[str|None]] = None
    background_color: str = "#ffffff"
    accents_color: str = "#ffffff"
    theme_type: str = "00"
    group_id: Union[str, None] = ""
    sub_group_id: Union[str, None] = ""
    hidden_phone: bool = False
    language: str = "vietnamese"
    primary_profile: bool = True

    widget_company: List[Widget_Company] = []
    widget_email: List[Widget_Email] = []
    widget_mobile: List[Widget_Mobile] = []
    widget_image_gallery: List[Widget_Image_Gallery] = []
    widget_social_network_link: List[Widget_Social_Network_Link] = []
    widget_custom_link: List[Widget_Custom_Link] = []
    group_info: Group_Info = None

class ProfileInfoModelRtn(ErrorMessageModel, ProfileInfoModel):
    
    # model_config = ConfigDict(
    #     arbitrary_types_allowed=True,
    #     populate_by_name=True,           # cho phép alias ngược lại khi dump
    #     extra="allow",
    #     json_encoders={ObjectId: str}    # chuyển ObjectId thành str khi dump ra JSON                
    # )

    # id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    account_mode: str = "free user"
    change_profile: bool = True
    # name: str = ""
    # designation: str = ""
    # bio: str = ""
    # area_code: str = ""
    # primary_mobile: str = ""
    # primary_email: str = ""
    # address: str = ""
    # slogan: str = ""
    # avatar_location: str = ""
    # banner_location: str = ""
    # backgroumd_color: str = "#ffffff"
    # accents_color: str = "#ffffff"
    # theme_type: str = "00"
    # group_id: Union[str, None] = ""
    # sub_group_id: Union[str, None] = ""
    # hidden_phone: bool = False
    # language: str = "vietnamese"
    # primary_profile: bool = True

    # widget_company: List[Widget_Company] = []
    # widget_email: List[Widget_Email] = []
    # widget_mobile: List[Widget_Mobile] = []
    # widget_image_gallery: List[Widget_Image_Gallery] = []
    # widget_social_network_link: List[Widget_Social_Network_Link] = []
    # widget_custom_link: List[Widget_Custom_Link] = []


class ProfileInfoCardModelRtn(ProfileInfoModelRtn):
    card_status: str = ""
    link_status: str = ""