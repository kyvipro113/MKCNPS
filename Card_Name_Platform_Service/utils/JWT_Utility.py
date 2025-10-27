from fastapi import HTTPException
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, UTC
import uuid
from Card_Name_Platform_Service.utils.Redis_Utility import *

# credentials_exception = HTTPException(
#     status_code=401,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )

SECRET_KEY = "728b47cdae4823d01dc5c36c95364680fb3af92307689afd21cd8106d7ff9dd3"
ALGORITHM = "HS256"

async def create_jwt_token(data: dict, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM, db=0):
    # Set the expiration time to 10 minutes from now
    expiration_time = datetime.now(UTC) + timedelta(minutes=60*24)
    # datetime.now(UTC) ### Using from python ver 3.11
    
    # Include the expiration time in the token payload
    data["exp"] = expiration_time
    # Unique identifier for the token
    data["jti"] = str(uuid.uuid4())
    print(f"JTI: {data['jti']}")  
    data["token_type"] = "access"
    # Add token to redis
    redis_client = RedisClient(db=db)
    await redis_client.set(key=data["jti"], value="allow", ex=60*60*24)
    # Encode the token with the updated payload
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def create_jwt_access_and_refresh_token(data: dict, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM, remaining_time=-1, db=0):
    redis_client = RedisClient(db=0)
    access_exp = datetime.now(UTC) + timedelta(minutes=60*24)
    refresh_exp: datetime
    if remaining_time != -1:
        refresh_exp = remaining_time
    else:
        refresh_exp = datetime.now(UTC) + timedelta(days=30)

    data["exp"] = access_exp
    jti_access = str(uuid.uuid4())
    data["jti"] = jti_access
    print(f"JTI: {data['jti']}")
    data["token_type"] = "access"
    await redis_client.set(key=jti_access, value="allow", ex=60*60*24)
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    data["exp"] = refresh_exp
    jti_refresh = str(uuid.uuid4())
    data["jti"] = jti_refresh
    print(f"JTI: {data['jti']}")
    data["token_type"] = "refresh"
    await redis_client.set(key=jti_refresh, value="allow refresh", ex=60*60*24*30)
    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    jti1 = await redis_client.get(key=jti_access)
    jti2 = await redis_client.get(key=jti_refresh)

    print(f"Access token JTI in redis: {jti1}")
    print(f"Refresh token JTI in redis: {jti2}")

    return access_token, refresh_token

def decode_jwt_token(token: str, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise e
    