from typing import Type, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.JWT_Utility import decode_jwt_token
from Card_Name_Platform_Service.utils.Custom_HTTPException import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token_factory(model_cls: Type[BaseModel], mode: str = "all"):
    async def _verify_token(token: str = Depends(oauth2_scheme))->Union[PayloadEndUserModel, PayloadManagerModel, TokenPayloadModel]:
        if not isinstance(token, str) or not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=model_cls(message="Missing or invalid token type").model_dump(mode="json")
            )

        try:
            payload = decode_jwt_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=model_cls(message="Token can not decode").model_dump(mode="json")
            )

        if "uid" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=model_cls(message="Token is invalid").model_dump(mode="json")
            )

        uid = payload["uid"]
        if uid is None or uid == "":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=model_cls(message="Token is invalid").model_dump(mode="json")
                )

        # check is end user or manager
        if "change_profile" in payload:
            payload = PayloadEndUserModel(**payload)
        else:
            payload = PayloadManagerModel(**payload)

        if mode == "normal":
            return payload
        return TokenPayloadModel(token=token, payload=payload)
    return _verify_token

