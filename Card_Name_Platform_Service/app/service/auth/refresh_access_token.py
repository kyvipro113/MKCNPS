from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.utils.JWT_Utility import *

async def refresh_access_token(token_payload: TokenPayloadModel, ip: str):
    if token_payload.payload.token_type != "refresh":
        return JSONResponse(content=TokenModel(message=AuthMsg.invalid_refresh_token).model_dump(mode="json"), status_code=401)
    
    token_model = TokenModel()
    token_model.access_token = create_jwt_token(data=token_payload.payload.model_dump(mode="python"))
    token_model.refresh_token = token_payload.token
    token_model.message = AuthMsg.successful
    return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)
