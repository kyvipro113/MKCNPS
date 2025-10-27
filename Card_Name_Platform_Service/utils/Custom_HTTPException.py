from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Union

# class CustomHTTPException(HTTPException):
#     def __init__(self, status_code: int, message: str, model_cls: BaseModel):
#         super().__init__(status_code=status_code, detail=message)
#         self.code = code
    
#     def __str__(self):
#         return f"[HTTP {self.status_code}] {self.detail}"

#     def to_dict(self):
#         return {
#             "status_code": self.status_code,
#             "message": self.detail,
#             "code": self.code
#         }


class CustomHTTPException(JSONResponse, Exception):
    def __init__(self, status_code: int, content: Union[str, dict]):
        JSONResponse.__init__(self, content=content, status_code=status_code)
        Exception.__init__(self)