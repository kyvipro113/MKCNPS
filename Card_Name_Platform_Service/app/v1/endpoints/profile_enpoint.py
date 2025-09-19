from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.app.service.profile.get_profile_list import *

from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

@router.post("/get-profile-via-serial")
async def get_profile_via_serial(request: Request):
    ip = request.client.host

@router.post("/get-profile-via-username-link")
async def get_profile_via_username_link(request: Request):
    ip = request.client.host