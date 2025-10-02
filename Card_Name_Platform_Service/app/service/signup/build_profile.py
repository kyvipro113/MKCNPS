from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.Error_Msg import *

async def build_fast_profile(payload: PayloadEndUserModel, profile_built: ProfileInfoBuiltModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    
    try:
        oid = ObjectIdGenerator.generate(mode="oid")
        print(f"Generated OID: {oid}")
        avatar_locat = "avatar" + profile_built.avatar_name if profile_built.avatar_name != "" else ""
        banner_locat = "banner" + profile_built.banner_name if profile_built.banner_name != "" else ""
        profile_if = profile_info(
            id=oid,
            uid=payload.uid,
            name=profile_built.name,
            area_code=profile_built.area_code,
            primary_mobile=profile_built.primary_mobile,
            primary_email=profile_built.primary_email,
            address=profile_built.address,
            avatar_location=avatar_locat,
            banner_location=banner_locat,
            language=profile_built.language,
        )

        _oid = await mongo.insert_one(profile_info.__name__, profile_if.model_dump(mode="python", by_alias=True))
        print(f"Inserted profile ID: {_oid}")
        await mongo.update_one(account_info.__name__, payload.uid, {"username_link": profile_built.username_link})
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.build_successful).model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in build_profile - prepare data: {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.build_failed).model_dump(mode="json"), status_code=400)
        

    
    
