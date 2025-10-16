from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Card_Info_Model import *

async def linking_profile_to_card(payload: PayloadEndUserModel, card_if_model: Card_Info_Model, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        query = {
            "card_id": card_if_model.card_id,
            "pin": card_if_model.pin
        }
        card_if = await mongo.find_one(card_info.__name__, query)
        if card_if is None:
            return JSONResponse(content=ErrorMessageModel(message=CardMsg.not_found).model_dump(mode="json"), status_code=403)
        card_if = card_info(**card_if)
        if card_if.uid != "":
            return JSONResponse(content=ErrorMessageModel(message=CardMsg.is_linked).model_dump(mode="json"), status_code=402)
        await mongo.update_one(card_info.__name__, card_if.id, {"uid": payload.uid, "status": "00"})
        return JSONResponse(content=ErrorMessageModel(message=CardMsg.link_successful).model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in link_profile_to_card - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=CardMsg.link_successful).model_dump(mode="json"), status_code=400)
    

async def unlinking_profile_to_card(payload: PayloadEndUserModel, card_id: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        query = {
            "card_id": card_id,
            "uid": payload.uid
        }
        card_if = await mongo.find_one(card_info.__name__, query)
        if card_if is None:
            return JSONResponse(content=ErrorMessageModel(message=CardMsg.not_found).model_dump(mode="json"), status_code=403)
        card_if = card_info(**card_if)
        if card_if.uid == "" and card_if.status == "01":
            return JSONResponse(content=ErrorMessageModel(message=CardMsg.is_unlinked).model_dump(mode="json"), status_code=402)
        await mongo.update_one(card_info.__name__, card_if.id, {"uid": "", "status": "01"})
        # if card_if.group_id != "":
        #     condition = {
        #         "uid": payload.uid
        #     }
        #     update_field = {
        #         "group_id": "",
        #     }
        #     await mongo.update_many(profile_info.__name__, condition, update_field)

        return JSONResponse(content=ErrorMessageModel(message=CardMsg.unlink_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in unlink_profile_to_card - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=CardMsg.unlink_failed).model_dump(mode="json"), status_code=400)
    