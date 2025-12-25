from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Card_Info_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *

async def get_list_card(payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        pipeline = [
            {"$match": {"uid": payload.uid}},
            {
                "$project": {
                    "card_id": 1,
                    "status": 1
                }
            }
        ]
        card_list = await mongo.aggregate(card_info.__name__,pipeline)
        card_serials = [Card_Serial_Info_Model(**card) for card in card_list]

        pipeline_avatar = [
            {"$match": {
                "uid": payload.uid, 
                "primary_profile": True
                }
            },
            {
                "$project": {
                    "avatar_location": 1
                }
            }
        ]
        profile = await mongo.aggregate(profile_info.__name__, pipeline_avatar)
        avatar_location = (profile[0].get("avatar_location", None))
        
        if avatar_location:
            folder_file_obj = avatar_location.split("/")
            avatar_location = await Minio_Client.get_url(bucket_name=folder_file_obj[0], object_name=folder_file_obj[1])

        card_list_model = Card_List_Model(cards=card_serials, avatar_location=avatar_location, message=CardMsg.get_list_card_successful)
        return JSONResponse(content=card_list_model.model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in get_list_card: {str(e)}")
        return JSONResponse(content=Card_List_Model(message=CardMsg.get_list_card_failed).model_dump(mode="json"), status_code=500)