from fastapi import APIRouter, Request, Depends
from Card_Name_Platform_Service.app.model.Register_Model import *
from Card_Name_Platform_Service.app.service.signup.signup import *
from Card_Name_Platform_Service.app.service.signup.verify_and_register import *
from Card_Name_Platform_Service.app.service.signup.build_profile import *
from Card_Name_Platform_Service.utils.Auth_Utility import *



router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)

@router.post("/register-account",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def register_account(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await signup(auth=auth_model, ip=ip)
    return res

@router.post("/verify-account/{verification_code}",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def verify_account(request: Request, verification_code: str, payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal", is_pop_redis=True))):
    ip = request.client.host
    res = await verify_and_register(verify_code=verification_code, payload=payload, ip=ip)
    return res
