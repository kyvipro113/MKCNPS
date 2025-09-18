from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *

from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def login(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await authenticate_user(auth_model, ip)
    return res

@router.post("/cms-login")
async def cms_login(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await authenticate_user(auth_model, ip, mode="cms")
    return res

@router.post("/refresh-token")
async def refresh_token(request: Request, token_payload=Depends(verify_token_factory(TokenModel, mode="all"))):
    ip = request.client.host
    res = await refresh_access_token(token_payload=token_payload, ip=ip)
    return res
