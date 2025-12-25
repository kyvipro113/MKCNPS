from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.service.auth.forgot_password import *

from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def login(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await authenticate_user(auth_model, ip)
    return res

@router.post("/cms-login",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def cms_login(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await authenticate_user(auth_model, ip, mode="cms")
    return res

@router.post("/refresh-token",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def refresh_token(request: Request, token_payload: TokenPayloadModel=Depends(verify_token_factory(TokenModel, mode="all"))):
    ip = request.client.host
    res = await refresh_access_token(token_payload=token_payload, ip=ip)
    return res

@router.post("/find-password",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
             )
async def find_password(request: Request):
    ip = request.client.host
    req = await request.json()
    email = req.get("email", "")
    res = await find_password_endpoint(email=email, ip=ip)
    return res

@router.post("/reset-password",
             responses={
                 200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                 400: {"model": TokenModel, "description": "Bad Request"}
             })
async def reset_password(request: Request, token_payload: TokenPayloadModel=Depends(verify_token_factory(TokenModel, mode="all"))):
    ip = request.client.host
    req = await request.json()
    verify_code = req.get("verify_code", "")
    new_password = req.get("new_password", "")
    res = await reset_password_endpoint(payload=token_payload.payload, verify_code=verify_code, new_password=new_password, ip=ip)
    return res