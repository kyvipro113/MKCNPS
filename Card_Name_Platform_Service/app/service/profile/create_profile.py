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

async def create_profile(payload: PayloadEndUserModel, profile_info_built: ProfileInfoBuiltModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        profile_if = profile_info(**profile_info_built.model_dump(mode="python", by_alias=True))
        profile_if.id = ObjectIdGenerator.generate()
        profile_if.uid = payload.uid

        if profile_info_built.avatar_name != None and profile_info_built.avatar_name != "":
            await Minio_Client.move_object(src_bucket="temp", src_object=profile_info_built.avatar_name, dest_bucket="avatar")
            profile_if.avatar_location = "avatar/" + profile_info_built.avatar_name
            delattr(profile_if, "avatar_name")
            
        if profile_info_built.banner_name != None and profile_info_built.banner_name != "":
            if len(profile_info_built.banner_name) == 7 and profile_info_built.banner_name[0].startswith("#"):
                profile_if.banner_location = profile_info_built.banner_name
            else:
                await Minio_Client.move_object(src_bucket="temp", src_object=profile_info_built.banner_name, dest_bucket="banner")
                profile_if.banner_location = "banner/" + profile_info_built.banner_name
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

        _oid = await mongo.insert_one(profile_info.__name__, profile_if.model_dump(mode="python", by_alias=True))
        print(f"Inserted profile ID: {_oid}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.create_new_profile_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in create_profile - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.create_new_profile_failed).model_dump(mode="json"), status_code=400)