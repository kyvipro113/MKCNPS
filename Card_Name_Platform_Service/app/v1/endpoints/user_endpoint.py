from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *

from Card_Name_Platform_Service.app.service.signup.signup import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.service.profile.get_profile_list import *
from Card_Name_Platform_Service.app.service.signup.verify_and_register import *
from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/sign-up",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    403: {"model": TokenModel, "description": "Forbidden"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def sign_up(request: Request, auth_model: AuthModel):
    ip = request.client.host
    res = await signup(auth_model, ip)
    return res

# @router.post("/verify-account/{verification_code}",
#                 responses={
#                     200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
#                     401: {"model": TokenModel, "description": "Unauthorized"},
#                     400: {"model": TokenModel, "description": "Bad Request"}
#                 }
#             )
# async def verify_account(request: Request, verification_code: str, payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal", is_pop_redis=True))):
#     ip = request.client.host
#     res = await verify_and_register(verify_code=verification_code, payload=payload, ip=ip)
#     return res
 
@router.post("/verify-account/{verification_code}",
                responses={
                    200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
                    401: {"model": TokenModel, "description": "Unauthorized"},
                    400: {"model": TokenModel, "description": "Bad Request"}
                }
            )
async def verify_account(request: Request, verification_code: str, card_id: str|None=None, pin: str|None=None, payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal", is_pop_redis=True))):
    ip = request.client.host
    res = await verify_and_register(verify_code=verification_code, payload=payload, ip=ip, card_id=card_id, pin=pin)
    return res


# @router.post("/send-verify-code-to-email")
# async def send_verify_code_to_email(request: Request):
#     ip = request.client.host

# @router.post("/verify-register-email")
# async def verify_register_email(request: Request):
#     ip = request.client.host

# @router.post("/create-fast-profile")
# async def create_fast_profile(request: Request, token_payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal"))):
#     ip = request.client.host

# @router.post("link-profile-to-card")
# async def link_profile_to_card(request: Request, token_payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal"))):
#     ip = request.client.host

# @router.post("/get-profile-list")
# async def get_profile_list(request: Request, token_payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal"))):
#     ip = request.client.host
#     print(token_payload)
#     res = await get_profile_list(uid=token_payload.uid, ip=ip)
#     return JSONResponse(content="OK", status_code=200)
    
