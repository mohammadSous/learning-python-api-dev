import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME


SECRET_KEY = "986395efcee6f1c3fdaec5ebe3b7548a66ef812cd7cf2d4febb892efe5ffa9e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() # takes the entred data which is the user id.

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # adds expire to the dict (to_encode)

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM) # jwt method that takes the payload, key (secret), and the algorithm.
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(ouath2_scheme)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't validate credentials.", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)