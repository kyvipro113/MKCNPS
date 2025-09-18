from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.app.service.profile.get_profile_list import *

from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/get-profile-list")
async def get_profile_list(request: Request, token_payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal"))):
    ip = request.client.host
    print(token_payload)
    res = await get_profile_list(uid=token_payload.uid, ip=ip)
    return JSONResponse(content="OK", status_code=200)
    
