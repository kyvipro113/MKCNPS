from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from typing import Type, Union


async def get_detail_profile(key: str, ip: str, model_cls: Type[Union[ProfileInfoModelRtn, ProfileInfoCardModelRtn]], optional=0, **kwargs):
    # Optional 0: by profile_id & uid, optional 1: by serial number, optional 2: by username link
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        profile_if_rtn: Union[ProfileInfoModelRtn, ProfileInfoCardModelRtn] = None
        if optional == 0:
            print(kwargs)
            payload: PayloadEndUserModel = kwargs.get("payload", None)
            pipeline = [
                {
                    "$match": {
                        "_id": ObjectId(payload.uid)
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "change_profile": 1,
                        "account_mode": 1
                    }
                }
            ]
            data = await mongo.aggregate(account_info.__name__, pipeline)
            print(data)
            # profile_if_rtn = ProfileInfoModelRtn(**data[0])
            # print(profile_if_rtn)

            query = {
                "_id": ObjectId(key),
                "uid": payload.uid
            }
            projection = {
                "uid": 0
            }
            profile_if = await mongo.find_one(profile_info.__name__, query, projection=projection)
            if profile_if is None:
                return JSONResponse(content=ProfileInfoModelRtn(**data[0], message=ProfileMsg.not_found).model_dump(mode="json"), status_code=499)
            
            profile_if_rtn = ProfileInfoModelRtn(**data[0], **profile_if, message=ProfileMsg.get_successful)

        elif optional == 1:
            print(kwargs)
            language: str = kwargs.get("language", None)
            query = {
                "card_id": key,
            }
        
            data = await mongo.find_one(card_info.__name__, query)
            if data is None:
                return JSONResponse(content=model_cls(message=CardMsg.not_found).model_dump(mode="json"), status_code=499)
        
            card_if = card_info(**data)
            if card_if.uid is None or card_if.uid == "":
                return JSONResponse(content=model_cls(card_status=CardMsg.is_found, message=CardMsg.is_unlinked).model_dump(mode="json"), status_code=498)

            query = {
                "uid": card_if.uid,
                "primary_profile": True
            } if language is None or language == "" else {
                "uid": card_if.uid,
                "primary_profile": True,
                "language": language
            }

            projection = {
                "uid": 0
            }

            profile_if = await mongo.find_one(profile_info.__name__, query, projection=projection)
            if profile_if is None:
                return JSONResponse(content=model_cls(card_status=CardMsg.is_found, message=ProfileMsg.not_found).model_dump(mode="json"), status_code=499)
            
            profile_if_rtn = model_cls(**profile_if, card_status=CardMsg.is_found, link_status=CardMsg.is_linked, message=ProfileMsg.get_successful)

        ## Group
        if profile_if_rtn.group_id is not None and profile_if_rtn.group_id != "":
            query = {
                "group_id": profile_if_rtn.group_id,
                "language": profile_if_rtn.language
            }
            projection = {
                "group_id": 0
            }
            group_if = await mongo.find_one(group_info.__name__, query, projection=projection)
            if group_if is not None:
                profile_if_rtn.group_info = Group_Info(**group_if)


        folder_file_obj = profile_if_rtn.avatar_location.split('/')
        if profile_if_rtn.avatar_location != "":
            profile_if_rtn.avatar_location = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1])
        
        folder_file_obj = profile_if_rtn.banner_location.split('/')
        if profile_if_rtn.banner_location != "":
            profile_if_rtn.banner_location = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1])

        if len(profile_if_rtn.widget_company) != 0:
            for idx, comp in enumerate(profile_if_rtn.widget_company):
                if comp.company_logo != "":
                    folder_file_obj = comp.company_logo.split('/')
                    profile_if_rtn.widget_company[idx].company_logo = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1]) 

        if len(profile_if_rtn.widget_image_gallery) != 0:
            for idx, img in enumerate(profile_if_rtn.widget_image_gallery):
                if len(img.image_locations) != 0:
                    for idxx, img_loc in enumerate(img.image_locations):
                        folder_file_obj = img_loc.split('/')
                        profile_if_rtn.widget_image_gallery[idx].image_locations[idxx] = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1])
            
        if profile_if_rtn.group_info is not None:
            if profile_if_rtn.group_info.group_logo != "":
                folder_file_obj = profile_if_rtn.group_info.group_logo.split('/')
                profile_if_rtn.group_info.group_logo = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1])
                

        return JSONResponse(content=profile_if_rtn.model_dump(mode="json"), status_code=200)
        
        

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in get_detail_profile - optional {optional}: {str(e)}")
        return JSONResponse(content=model_cls(message=ProfileMsg.get_failed).model_dump(mode="json"), status_code=400)
        
    