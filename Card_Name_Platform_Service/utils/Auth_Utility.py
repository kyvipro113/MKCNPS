
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer
# from Card_Name_Platform_Service.utils.JWT_Utility import *
# from Card_Name_Platform_Service.app.model.Token_Model import *

# SECRET_KEY = "728b47cdae4823d01dc5c36c95364680fb3af92307689afd21cd8106d7ff9dd3"
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_token(_class: BaseModel, token: str=Depends(oauth2_scheme), mode="all"):
#     payload = {}
#     try:
#         payload = decode_jwt_token(token, SECRET_KEY, ALGORITHM)
#     except Exception as e:
#         raise HTTPException(
#             status_code=401,
#             detail=_class(message="Token can not decode").model_dump(mode="json")
#         )
#         #raise JSONResponse(content=_class(message="Token can not decode").model_dump(mode="json"), status_code=401)
#     uid = payload.get("uid")
#     if uid is None:
#         raise HTTPException(
#             status_code=401,
#             detail=_class(message="Token is invalid").model_dump(mode="json")
#         )

#         #raise JSONResponse(content=_class(message="Token is invalid").model_dump(mode="json"), status_code=401)
#     if mode == "normal":
#         return payload
#     return {"payload": payload, "token": token}


from typing import Type, Union
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.JWT_Utility import decode_jwt_token
from Card_Name_Platform_Service.utils.Custom_HTTPException import *

SECRET_KEY = "728b47cdae4823d01dc5c36c95364680fb3af92307689afd21cd8106d7ff9dd3"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token_factory(mode: str = "all"):
    async def _verify_token(token: str = Depends(oauth2_scheme))->Union[PayloadEndUserModel, PayloadManagerModel, TokenPayloadModel]:
        if not isinstance(token, str) or not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid token type"
            )

            #raise JSONResponse(content=model_cls(message="Token can not decode").model_dump(mode="json"), status_code=401)
            #raise CustomHTTPException(content=model_cls(message="Token can not decode").model_dump(mode="json"), status_code=401)

        try:
            payload = decode_jwt_token(token, SECRET_KEY, ALGORITHM)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token can not decode"
            )

            #raise JSONResponse(content=model_cls(message="Token can not decode").model_dump(mode="json"), status_code=401)

            #raise CustomHTTPException(content=model_cls(message="Token can not decode").model_dump(mode="json"), status_code=401)



        uid = payload["uid"]
        print(f"Debug: payload={payload}")
        if uid is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid"
            )

            #raise JSONResponse(content=model_cls(message="Token is invalid").model_dump(mode="json"), status_code=401)

            #raise CustomHTTPException(content=model_cls(message="Token can not decode").model_dump(mode="json"), status_code=401)

        # check is end user or manager
        if payload["change_profile"] is not None:
            payload = PayloadEndUserModel(**payload)
        else:
            payload = PayloadManagerModel(**payload)

        if mode == "normal":
            return payload
        return TokenPayloadModel(token=token, payload=payload)
    return _verify_token

