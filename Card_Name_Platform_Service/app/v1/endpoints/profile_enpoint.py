from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.app.service.profile.get_profile_list import *
from Card_Name_Platform_Service.app.service.profile.get_detail_profile import *
from Card_Name_Platform_Service.app.service.profile.build_profile import *
from Card_Name_Platform_Service.app.service.profile.linking_profile import *

from Card_Name_Platform_Service.utils.Auth_Utility import *

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

@router.post("/build-profile")
async def build_profile(request: Request, profile_built: ProfileInfoBuiltModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await build_fast_profile(payload=payload, profile_built=profile_built, ip=ip)
    return res

@router.post("/link-profile-to-card")
async def link_profile_to_card(request: Request, card_if_model: Card_Info_Model, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await linking_profile_to_card(payload=payload, card_if_model=card_if_model, ip=ip)
    return res

@router.post("/unlink-profile-to-card/{card_id}")
async def unlink_profile_to_card(request: Request, card_id: str, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await unlinking_profile_to_card(payload=payload, card_id=card_id, ip=ip)
    return res

@router.get("/get-profile-list")
async def get_profile_list(Request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = Request.client.host
    res = await get_profile_list_user(payload=payload, ip=ip)
    return res

@router.get("/get-profile-info/{profile_id}")
async def get_profile_info(request: Request, profile_id: str, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await get_detail_profile(key=profile_id, ip=ip, model_cls=ProfileInfoModelRtn, optional=0, payload=payload)
    return res

@router.get("/get-profile-info-via-serial/{card_id}")
async def get_profile_info_via_serial(request: Request, card_id: str):
    ip = request.client.host
    res = await get_detail_profile(key=card_id, ip=ip, model_cls=ProfileInfoCardModelRtn, optional=1)
    return res

@router.get("/get-profile-info-via-serial-with-language/{card_id}/{language}")
async def get_profile_info_via_serial_with_language(request: Request, card_id: str, language: str):
    ip = request.client.host
    res = await get_detail_profile(key=card_id, ip=ip, model_cls=ProfileInfoCardModelRtn, optional=1, language=language)
    return res
    

@router.get("/get-profile-info-via-username-link/{username_link}")
async def get_profile_via_username_link(request: Request, username_link: str, language: str|None=None):
    ip = request.client.host
    res = await get_detail_profile(key=username_link, ip=ip, model_cls=ProfileInfoModelRtn, optional=2, language=language)
    return res