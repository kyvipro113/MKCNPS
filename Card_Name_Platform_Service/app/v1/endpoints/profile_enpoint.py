from fastapi import APIRouter, Request

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Account_Info_Model import *
from Card_Name_Platform_Service.app.service.auth.authentication import *
from Card_Name_Platform_Service.app.service.auth.refresh_access_token import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.app.service.profile.get_profile_list import *
from Card_Name_Platform_Service.app.service.profile.create_profile import *
from Card_Name_Platform_Service.app.service.profile.get_detail_profile import *
from Card_Name_Platform_Service.app.service.profile.build_profile import *
from Card_Name_Platform_Service.app.service.profile.edit_profile import *
from Card_Name_Platform_Service.app.service.profile.linking_profile import *
from Card_Name_Platform_Service.app.service.profile.set_primary_profile import *
from Card_Name_Platform_Service.app.service.profile.delete_profile import *
from Card_Name_Platform_Service.app.service.profile.get_username_link_profile import *
from Card_Name_Platform_Service.app.service.profile.update_username_link import *
from Card_Name_Platform_Service.app.service.profile.get_list_card import *
from Card_Name_Platform_Service.app.service.profile.get_settings_account import *
from Card_Name_Platform_Service.app.service.profile.activate_deactivate_phone_login import *
from Card_Name_Platform_Service.app.service.profile.reset_setting_account import *

from Card_Name_Platform_Service.utils.Auth_Utility import *
from Card_Name_Platform_Service.app.service.sys.utils import *

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

@router.post("/create-new-profile")
async def create_new_profile(request: Request, profile_info_built: ProfileInfoBuiltModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await create_profile(payload=payload, profile_info_built=profile_info_built, ip=ip)
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

@router.post("/edit-profile")
async def edit_profile_info(request: Request, profile_info_edit_model: ProfileInfoEditModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await edit_profile(payload=payload, profile_info_edit_model=profile_info_edit_model, ip=ip)
    return res

@router.post("/set-primary-profile/{profile_id}")
async def set_primary_profile_endpoint(request: Request, profile_id: str, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await set_primary_profile(payload=payload, profile_id=profile_id, ip=ip)
    return res

@router.post("/delete-profile/{profile_id}")
async def delete_profile_endpoint(request: Request, profile_id: str, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await delete_profile(payload=payload, profile_id=profile_id, ip=ip)
    return res

@router.get("/get-username-link")
async def get_username_link(request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await get_username_link_profile(payload=payload, ip=ip)
    return res

@router.post("/update-username-link")
async def update_username_link_endpoint(request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    req = await request.json()
    new_username_link = req.get("new_username_link", "")
    res = await update_username_link(payload=payload, new_username_link=new_username_link, ip=ip)
    return res

@router.get("/get-list-card")
async def get_list_card_endpoint(request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await get_list_card(payload=payload, ip=ip)
    return res

@router.get("/get-account-settings")
async def get_account_settings_endpoint(request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await get_settings_account(payload=payload, ip=ip)
    return res

@router.post("/activate-deactivate-phone-login")
async def activate_deactivate_phone_login_endpoint(request: Request, data: AccountSettingsModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await activate_deactivate_phone_login(data=data, payload=payload, ip=ip)
    return res

@router.post("/reset-account-settings")
async def reset_account_settings_endpoint(request: Request, data: ResetSettingsModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await reset_setting_account(data=data, payload=payload, ip=ip)
    return res

@router.post("/send-verify-code")
async def send_verify_code_endpoint(request: Request, data: ResetSettingsModel, payload: PayloadEndUserModel=Depends(verify_token_factory(ErrorMessageModel, mode="normal"))):
    ip = request.client.host
    res = await send_verify_code(data=data, payload=payload, ip=ip)
    return res


@router.post("/translate-batch")
async def translate_profile_batch(request: Request):
    req = await request.json()
    texts = req.get("texts", [])
    source_language = req.get("source_language", "auto")
    target_language = req.get("target_language", "en")
    from Card_Name_Platform_Service.utils.Translate_Batch import translate_batch
    res = await translate_batch(texts=texts, source_language=source_language, target_language=target_language)
    return {"translations": res}