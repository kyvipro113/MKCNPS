from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.utils.Gen_Universal_UID import *
from Card_Name_Platform_Service.utils.Other_Utils import *

async def edit_profile(payload: PayloadEndUserModel, profile_info_edit_model: ProfileInfoEditModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        profile_if = profile_info(**profile_info_edit_model.model_dump(mode="python", by_alias=True))
        profile_if.uid = payload.uid
        profile_if.id = ObjectId(profile_if.id)

        if profile_info_edit_model.avatar_name != None and profile_info_edit_model.avatar_name != "":
            if profile_info_edit_model.avatar_name.startswith("http://") or profile_info_edit_model.avatar_name.startswith("https://"):
                profile_if.avatar_location = get_bucket_object_from_url(profile_info_edit_model.avatar_name, get_location=True)
            else:
                await Minio_Client.move_object(src_bucket="temp", src_object=profile_info_edit_model.avatar_name, dest_bucket="avatar")
                profile_if.avatar_location = "avatar/" + profile_info_edit_model.avatar_name
            
            delattr(profile_if, "avatar_name")
            
        if profile_info_edit_model.banner_name != None and profile_info_edit_model.banner_name != "":
            if profile_info_edit_model.banner_name.startswith("#") and len(profile_info_edit_model.banner_name) == 7:
                profile_if.banner_location = profile_info_edit_model.banner_name
            elif profile_info_edit_model.banner_name.startswith("http://") or profile_info_edit_model.banner_name.startswith("https://"):
                profile_if.banner_location = get_bucket_object_from_url(profile_info_edit_model.banner_name, get_location=True)
            else:
                await Minio_Client.move_object(src_bucket="temp", src_object=profile_info_edit_model.banner_name, dest_bucket="banner")
                profile_if.banner_location = "banner/" + profile_info_edit_model.banner_name
            
            delattr(profile_if, "banner_name")

        if hasattr(profile_if, "widget_company"):   ## CLS
            for idx, company_obj in enumerate(profile_if.widget_company):
                if "company_logo" in profile_if.widget_company[idx]: ## Key in dict
                    if profile_if.widget_company[idx]["company_logo"] != None and profile_if.widget_company[idx]["company_logo"] != "":
                        await Minio_Client.move_object(src_bucket="temp", src_object=profile_if.widget_company[idx]["company_logo"], dest_bucket="company")   
                        profile_if.widget_company[idx]["company_logo"] = "company/" + profile_if.widget_company[idx]["company_logo"] 
        
        if hasattr(profile_if, "widget_image_gallery"):
            for idx, img_gallery in enumerate(profile_if.widget_image_gallery):
                for idxx, img_locat in enumerate(img_gallery["image_locations"]):
                    if img_locat != None and img_locat != "":
                        await Minio_Client.move_object(src_bucket="temp", src_object=img_locat, dest_bucket="gallery")
                        profile_if.widget_image_gallery[idx]["image_locations"][idxx] = "gallery/" + img_locat

        count = await mongo.replace_one(profile_info.__name__, str(profile_if.id), profile_if.model_dump(mode="python", by_alias=True))
        print(f"Modified profile count: {count}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.edit_profile_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in edit_profile - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.edit_profile_failed).model_dump(mode="json"), status_code=400)