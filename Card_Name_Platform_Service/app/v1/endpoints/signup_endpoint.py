# from fastapi import APIRouter, Request, Depends, Query
# from Card_Name_Platform_Service.app.model.Register_Model import *
# from Card_Name_Platform_Service.app.service.signup.signup import *
# from Card_Name_Platform_Service.app.service.signup.verify_and_register import *
# from Card_Name_Platform_Service.app.service.profile.build_profile import *
# from Card_Name_Platform_Service.utils.Auth_Utility import *
# from typing import Union


# router = APIRouter(
#     prefix="/signup",
#     tags=["signup"]
# )

# @router.post("/register-account",
#                 responses={
#                     200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
#                     401: {"model": TokenModel, "description": "Unauthorized"},
#                     400: {"model": TokenModel, "description": "Bad Request"}
#                 }
#             )
# async def register_account(request: Request, auth_model: AuthModel):
#     ip = request.client.host
#     res = await signup(auth=auth_model, ip=ip)
#     return res

# @router.post("/verify-account/{verification_code}",
#                 responses={
#                     200: {"model": TokenModel, "description": "Successful", "include_in_schema": False},
#                     401: {"model": TokenModel, "description": "Unauthorized"},
#                     400: {"model": TokenModel, "description": "Bad Request"}
#                 }
#             )
# async def verify_account(request: Request, verification_code: str, card_id: str|None=Query(None), pin: str|None=Query(None), payload: PayloadEndUserModel=Depends(verify_token_factory(TokenModel, mode="normal", is_pop_redis=True))):
#     ip = request.client.host
#     print(f"Card id: {card_id}, Pin: {pin}")
#     if card_id is None:
#         print("No card id provided")
#     else:
#         print("Card id OK")
#     res = await verify_and_register(verify_code=verification_code, payload=payload, ip=ip, card_id=card_id, pin=pin)
#     return res


# @router.post("/test-verify/{verification_code}")
# async def test_verify(request: Request, verification_code: str, card_id: str):
#     ip = request.client.host
#     print(f"Card id: {card_id}")
#     res = {"message": "Test verify endpoint", "verification_code": verification_code, "card_id": card_id, "ip": ip}
#     return res
