from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.utils.JWT_Utility import *

from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Register_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.utils.Redis_Utility import *
from Card_Name_Platform_Service.app.service.sys.utils import send_verification_code
import uuid

async def signup(auth: AuthModel, ip: str):
    mongo = AsyncMongoDB()
    redis_client = RedisClient()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    uid = str(ObjectIdGenerator.generate(mode="oid"))
    print(f"uid gen: {uid}")
    account_if = account_info(id=uid, email=auth.email, pwd=auth.password)
    try:
        # check existing email
        query = {"email": auth.email}
        acc_if_ck = await mongo.find_one(account_info.__name__, query)
        if acc_if_ck is not None:
            return JSONResponse(content=TokenModel(message=RegisterMsg.email_exist).model_dump(mode="json"), status_code=403)

        # oid = await mongo.insert_one(account_info.__name__, account_if.model_dump(mode="python", by_alias=True))
        # print(f"Inserted ID: {oid}")
        
        # Add temp account to redis
        await redis_client.set_json(key=uid, value=account_if.model_dump(mode="python", by_alias=True), ex=600)
        token_data = PayloadEndUserModel(
            uid=uid,
            flag=account_if.first_login,
            change_profile=account_if.change_profile
        )

        # Send verification code to email
        verification_code_id = str(uuid.uuid4())
        token_data.model_extra["code_id"] = verification_code_id
        token_data.model_extra["email"] = account_if.email
        await send_verification_code(code_id=verification_code_id, email=account_if.email, ip=ip, mode="register")

        token_model = TokenModel()
        token_model.access_token = await create_jwt_token(data=token_data.model_dump(mode="python"))
        token_model.message = RegisterMsg.successful
        return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in signup: {str(e)}")
        return JSONResponse(content=TokenModel(message=RegisterMsg.failed).model_dump(mode="json"), status_code=400)