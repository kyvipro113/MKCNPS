from fastapi import HTTPException
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, UTC

# credentials_exception = HTTPException(
#     status_code=401,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )

SECRET_KEY = "728b47cdae4823d01dc5c36c95364680fb3af92307689afd21cd8106d7ff9dd3"
ALGORITHM = "HS256"

def create_jwt_token(data: dict, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM):
    # Set the expiration time to 10 minutes from now
    expiration_time = datetime.now(UTC) + timedelta(minutes=60*25)
    # datetime.now(UTC) ### Using from python ver 3.11
    
    # Include the expiration time in the token payload
    data["exp"] = expiration_time
    
    # Encode the token with the updated payload
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_jwt_access_and_refresh_token(data: dict, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM, remaining_time=-1):
    access_exp = datetime.now(UTC) + timedelta(minutes=60*25)
    refresh_exp: datetime
    if remaining_time != -1:
        refresh_exp = remaining_time
    else:
        refresh_exp = datetime.now(UTC) + timedelta(days=30)

    data["exp"] = access_exp
    data["token_type"] = "access"
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    data["exp"] = refresh_exp
    data["token_type"] = "refresh"
    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token

def decode_jwt_token(token: str, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise e
    