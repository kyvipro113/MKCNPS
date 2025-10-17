from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.utils.Redis_Utility import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.sys.utils import *
from Card_Name_Platform_Service.utils.JWT_Utility import *

async def verify_and_register(verify_code: str, payload: PayloadEndUserModel, ip: str, **kwargs):
    mongo = AsyncMongoDB()
    redis = RedisClient()
    logger = Logger(folder_name="Log", file_name="verify_and_register", name_logger="verify_and_register", file_mode="a")
    token_model = EndUserTokenModelRtn()
    try:
        print(payload)
        verified = await verify_code_check(code_id=payload.code_id, email=payload.email, verify_code=verify_code, ip=ip)
        if not verified:
            return JSONResponse(content=EndUserTokenModelRtn(message=RegisterMsg.verify_code_invalid).model_dump(mode="json"), status_code=403)
        # Get temp account from redis
        account_if = await redis.pop_json(key=payload.uid)
        if account_if is None:
            return JSONResponse(content=EndUserTokenModelRtn(message=RegisterMsg.handle_error).model_dump(mode="json"), status_code=400)
        
        account_if = account_info(**account_if)
        
        # Check card & pin if provided (for card of group)
        print(kwargs)
        card_id = kwargs.get("card_id", "")
        pin = kwargs.get("pin", "")
        if card_id != "" and pin != "":
            query = {
                "card_id": card_id,
                "pin": pin
            }
            card_if = await mongo.find_one(card_info.__name__, query)
            if card_if is not None:
                card_if = card_info(**card_if)
                if card_if.uid == "":
                    account_if.group_id = card_if.group_id
                    await mongo.update_one(card_info.__name__, card_if.id, {"uid": account_if.id, "status": "00"})
                    account_if.account_mode = "group user"
                    account_if.change_profile = card_if.change_profile

        account_if.id = ObjectId(account_if.id)          
        oid = await mongo.insert_one(account_info.__name__, account_if.model_dump(mode="python", by_alias=True))
        print(f"Inserted ID: {oid}")
        print(f"UID: {account_if.id}")

        token_data = PayloadEndUserModel(
            uid=payload.uid,
            email=account_if.email,
            # flag=account_if.first_login,
            # change_profile=account_if.change_profile
        )
        token_model.access_token, token_model.refresh_token = await create_jwt_access_and_refresh_token(data=token_data.model_dump(mode="python"))
        token_model.message = RegisterMsg.successful
        return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in verify_and_register: {str(e)}")
        return JSONResponse(content=EndUserTokenModelRtn(message=RegisterMsg.failed).model_dump(mode="json"), status_code=400)
    