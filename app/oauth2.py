import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME


SECRET_KEY = "986395efcee6f1c3fdaec5ebe3b7548a66ef812cd7cf2d4febb892efe5ffa9e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
