from typing import Type, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.JWT_Utility import *
from Card_Name_Platform_Service.utils.Custom_HTTPException import *
from Card_Name_Platform_Service.utils.Redis_Utility import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token_factory(model_cls: Type[BaseModel], mode: str = "all", is_pop_redis: bool = False):
    async def _verify_token(token: str = Depends(oauth2_scheme))->Union[PayloadEndUserModel, PayloadManagerModel, TokenPayloadModel]:
        if not isinstance(token, str) or not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=model_cls(message="Missing or invalid token type").model_dump(mode="json")
            )

        try:
            payload = decode_jwt_token(token)

            uid = payload["uid"]
            jti = payload["jti"]
            token_type = payload["token_type"]
            if uid is None or uid == "" or jti is None or jti == "" or token_type is None or token_type == "":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=model_cls(message="Token is invalid").model_dump(mode="json")
                )
            
            # Check token in redis
            expected_value = "allow" if token_type == "access" else "allow refresh"
            redis_client = RedisClient()
            alow_flag = await redis_client.assert_value(key=jti, expected_value=expected_value, is_pop=is_pop_redis)
            print(f"Token allow flag: {alow_flag}")
            if not alow_flag:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=model_cls(message="Token is revoked").model_dump(mode="json")
                )

            # check is end user or manager
            if payload["role"] == "user":
                payload = PayloadEndUserModel(**payload)
            else:
                payload = PayloadManagerModel(**payload)

            if mode == "normal":
                return payload
            return TokenPayloadModel(token=token, payload=payload)

        except Exception as e:
            print(f"Exception in verify_token_factory: {str(e)}")
            if isinstance(e, PyJWTError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=model_cls(message="Token can not decode").model_dump(mode="json")
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=model_cls(message="Token is invalid").model_dump(mode="json")
            )
        
    return _verify_token

