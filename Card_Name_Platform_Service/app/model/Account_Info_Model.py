from pydantic import BaseModel
from typing import Optional
from Card_Name_Platform_Service.app.model.Message_Model import *

class AccountSettingsModel(ErrorMessageModel):
    avatar_location: str = ""
    email: str = ""
    name: str = ""
    phone_number: str = ""
    act_login_by_phone_number: bool = True

class ResetSettingsModel(ErrorMessageModel):
    phone_number: Optional[str] = ""
    email: Optional[str] = ""
    old_password: Optional[str] = ""
    new_password: Optional[str] = ""
    otp: Optional[str] = ""
    flag: int = -1 # 0: phone_number, 1: email, 2: password