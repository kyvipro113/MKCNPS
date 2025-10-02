from pydantic import BaseModel, model_validator, Field, field_validator, ConfigDict
from typing import List, Dict, Any, Optional, Union
from bson import ObjectId


class account_info(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True           # cho phép alias ngược lại khi dump ## model.model_dump(mode="json", by_alias=True)
    )
    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    email: str = ""
    pwd: str = ""
    phone_number: str = ""
    username_link: str = ""
    language: str = "english"
    status: str = "02"
    act_login_by_phone_number: bool = False
    first_login: bool = False
    change_profile: bool = True

class manager_account(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True           # cho phép alias ngược lại khi dump
    )
    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    manager_user_name: str = ""
    manager_pwd: str = ""
    manager_email: str = ""
    manager_name: str = ""
    group_id: str = ""
    status: str = "00"

class card_info(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True           # cho phép alias ngược lại khi dump
    )
    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    card_id: str = ""
    uid: str = ""
    status: str = "01"
    pin: str = ""
 

class widget_company_branch(BaseModel):
    branch_name: str = ""
    area_code: str = ""
    phone: str = ""
    address_list: List[str] = []
    

class widget_company(BaseModel):
    company_name: str = ""
    company_logo: str = ""
    company_email: str = ""
    company_website: str = ""
    branch_list: List[widget_company_branch] = []
    layout_position: int = -1
    


class widget_custom_link(BaseModel):
    link_name: str = ""
    link_address: str = ""
    layout_position: int = -1

class widget_email(BaseModel):
    # model_config = ConfigDict(
    #     arbitrary_types_allowed=True,
    #     populate_by_name=True           # cho phép alias ngược lại khi dump
    # )
    # id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    # uid: str = ""

    email: str = ""
    layout_position: int = -1

class widget_image_gallery(BaseModel):
    image_locations: List[str] = []
    layout_position: int = -1

class widget_mobile(BaseModel):
    mobile_number: str = ""
    layout_position: int = -1

class widget_social_network_link(BaseModel):
    social_network_name: str = ""
    social_network_link: str = ""
    layout_position: int = -1
    
class group_branch(BaseModel):
    branch_name: str = ""
    branch_address: str = ""
    area_code_branch: str = ""
    branch_telephone: str = ""
    branch_email: str = ""
    branch_website: str = ""

class group_info(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True           # cho phép alias ngược lại khi dump
    )
    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    group_name: str = ""
    group_logo: str = ""
    group_branchs: List[group_branch] = []


class profile_info(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,           # cho phép alias ngược lại khi dump
        extra="allow"                   
    )

    id: Optional[Union[str, ObjectId]] = Field(default=None, alias="_id")
    uid: str = ""
    name: str = ""
    designation: str = ""
    bio: str = ""
    area_code: str = ""
    primary_mobile: str = ""
    primary_email: str = ""
    address: str = ""
    slogan: str = ""
    avatar_location: str = ""
    banner_location: str = ""
    backgroumd_color: str = "#ffffff"
    accents_color: str = "#ffffff"
    theme_type: str = "00"
    group_id: Union[str, None] = ""
    sub_group_id: Union[str, None] = ""
    hidden_phone: bool = False
    language: str = "vietnamese"
    primary_profile: bool = True
    
    # widgets_company: List[widget_company] = []
    # widgets_email: List[widget_email] = []
    # widgets_mobile: List[widget_mobile] = []
    # widgets_image_gallery: List[widget_image_gallery] = []
    # widgets_social_network_link: List[widget_social_network_link] = []
    # widgets_custom_link: List[widget_custom_link] = []

# if __name__ == "__main__":
#     data = {
#         "_id": ObjectId("68bfd71c651547d78cfdf59b"),
#         "uid": "68b1241c91b161bf70c9cf35",
#         "designation": "",
#         "bio": "No thing",
#         "area_code": "+84",
#         "primary_mobile": "386685086",
#         "primary_email": "marinkqh@gmail.com",
#         "address": "Thụy Sơn, Thái Thụy, Thái Bình",
#         "slogan": "Death is like the wind, always by my side",
#         "avatar_location": "avatar/3c990028f4f720250210164732_avatar.png",
#         "banner_location": "banner/3c990028f4f720250210164732_banner.png",
#         "background_color": "#ffffff",
#         "accents_color": "#000000",
#         "theme_type": "00",
#         "group_id": "",
#         "sub_group_id": "",
#         "hiden_phone": False,
#         "language": "vietnamese",
#         "primary_profile": True,
#         "widgets_company": [
#             {
#                 "company_name": "MKSmart JSC",
#                 "company_logo": "companygroup/17391601348955788_logo-mk-smart.png",
#                 "company_email": "info@mksmart.com.vn",
#                 "company_website": "https://mksmart.com.vn/",
#                 "branch_list": [
#                     {
#                         "area_code": "+84",
#                         "phone": "71006783",
#                         "branch_name": "Trụ sở chính",
#                         "address_list": [
#                             "Số 4, ngõ 15, Duy Tân, Cầu Giấy, Hà Nội",
#                             "Kcn, Quang Minh, Mê Linh, Hà Nội"
#                         ]
#                     },
#                     {
#                         "area_code": "+84",
#                         "phone": "39301055",
#                         "branch_name": "Chi nhánh Hồ Chí Minh",
#                         "address_list": [
#                             "Quận 9, Tp. Hồ Chí Minh",
#                             "Tp. Thủ Đức, Tp. Hồ Chí Minh"
#                         ]
#                     }
#                 ],
#                 "position": "Software Engineer",
#                 "layout_position": 1
#             }
#         ],
#         "widgets_email": [
#             {
#                 "email": "hongky260199@gmail.com",
#                 "layout_position": 2
#             },
#             {
#                 "email": "test1@gmail.com",
#                 "layout_position": 3
#             }
#         ],
#         "widgets_mobile": [
#             {
#                 "mobile_number": "0367964442",
#                 "layout_position": 4
#             },
#             {
#                 "mobile_number": "0398905181",
#                 "layout_position": 5
#             }
#         ],
#         "widgets_custom_link": [
#             {
#                 "link_name": "github.io",
#                 "link_address": "https://abcxyz.github.io",
#                 "layout_position": 6
#             },
#             {
#                 "link_name": "blog",
#                 "link_address": "https://bloguvt.wordpress.com",
#                 "layout_position": 7
#             }
#         ],
#         "widgets_image_gallery": [
#             {
#                 "image_locations": [
#                     "gallery/08c18cac20240919083703_gallery.png",
#                     "gallery/09af9ae420240919084552_gallery.png"
#                 ],
#                 "layout_position": 8
#             }
#         ],
#         "widgets_social_network_link": [
#             {
#                 "social_network_name": "Facebook",
#                 "social_network_link": "https://facebook.com/nevermore.169",
#                 "layout_position": 9
#             },
#             {
#                 "social_network_name": "social_network_name",
#                 "social_network_link": "https://tiktok.com/12131313",
#                 "layout_position": 10
#             }
#         ],
#             "name": "John Smith"
#     }
    
#     profile_if = profile_info(**data)
#     print(profile_if.model_dump(mode="python", by_alias=True))