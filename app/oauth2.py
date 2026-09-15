import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME


SECRET_KEY = "986395efcee6f1c3fdaec5ebe3b7548a66ef812cd7cf2d4febb892efe5ffa9e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict): # <<-- this happens after a successful login using POST /login
    to_encode = data.copy() # takes the entred data which is the user id.

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # adds expire to the dict (to_encode)

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM) # jwt method that takes the payload, key (secret), and the algorithm.
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # example: payload = {"user_id": 5, "exp": 1234567890
        id: str = payload.get("user_id") # example:  id = 5 (integer)

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # assigns it to token_data. Pydantic validates the shape the moment it's constructed
    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(ouath2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't validate credentials.", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user