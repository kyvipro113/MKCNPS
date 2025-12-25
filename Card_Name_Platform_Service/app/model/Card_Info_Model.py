from pydantic import BaseModel, model_validator
from typing import List, Dict, Any, Optional
from Card_Name_Platform_Service.app.model.Message_Model import *

class Card_Info_Model(BaseModel):
    card_id: str = ""
    pin: str = ""

class Card_Info_Ext_Model(Card_Info_Model):
    group_code: str = ""

class Card_Serial_Info_Model(BaseModel):
    card_id: str = ""
    status: str = ""

class Card_List_Model(ErrorMessageModel):
    cards: List[Card_Serial_Info_Model] = []
    avatar_location: Optional[str] = None