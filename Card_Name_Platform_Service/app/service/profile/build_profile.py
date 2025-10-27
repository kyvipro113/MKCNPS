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

async def build_fast_profile(payload: PayloadEndUserModel, profile_built: ProfileInfoBuiltModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    
    try:
        ## Check account link to card has group id
        card_if = await mongo.find_one(card_info.__name__, {"uid": payload.uid})
        card_if = card_info(**card_if) if card_if is not None else None
        group_id: str = card_if.group_id if card_if is not None else ""
        
        oid = ObjectIdGenerator.generate(mode="oid")
        print(f"Generated OID: {oid}")
        avatar_locat = "avatar/" + profile_built.avatar_name if profile_built.avatar_name != None and profile_built.avatar_name != "" else ""
        if profile_built.banner_name.startswith("#") and len(profile_built.banner_name) == 7:
            banner_locat = profile_built.banner_name
        else:
            banner_locat = "banner/" + profile_built.banner_name if profile_built.banner_name != None and profile_built.banner_name != "" else ""
        
        profile_if = profile_info(
            id=oid,
            uid=payload.uid,
            name=profile_built.name,
            designation=profile_built.designation,
            bio=profile_built.bio,
            area_code=profile_built.area_code,
            primary_mobile=profile_built.primary_mobile,
            primary_email=profile_built.primary_email,
            address=profile_built.address,
            avatar_location=avatar_locat,
            banner_location=banner_locat,
            language=profile_built.language,
            group_id=group_id
        )

        _oid = await mongo.insert_one(profile_info.__name__, profile_if.model_dump(mode="python", by_alias=True))
        print(f"Inserted profile ID: {_oid}")
        # check exists username link
        count_username_link = await mongo.count_documents(account_info.__name__, {"username_link": profile_built.username_link})
        print(count_username_link)
        if count_username_link > 0:
            return JSONResponse(content=ErrorMessageModel(message=UsernameLinkMsg.is_exists).model_dump(mode="json"), status_code=497)
        
        username_link = profile_built.username_link if profile_built.username_link != "" and profile_built.username_link != None else genUIDHex()
        update_fields = {
            "username_link": username_link,
            "phone_number": profile_built.primary_mobile,
        }
        await mongo.update_one(account_info.__name__, payload.uid, update_fields)
        
        # Move object from temp to permanent location in MinIO
        if profile_if.avatar_location.startswith("avatar/"):
            await Minio_Client.move_object(src_bucket="temp", src_object=profile_built.avatar_name, dest_bucket="avatar")

        if profile_if.banner_location.startswith("banner/"):
            await Minio_Client.move_object(src_bucket="temp", src_object=profile_built.banner_name, dest_bucket="banner")

        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.build_successful).model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in build_profile - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.build_failed).model_dump(mode="json"), status_code=400)
        

    
    
