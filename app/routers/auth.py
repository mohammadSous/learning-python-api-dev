from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # username and password.


router = APIRouter(prefix= "/login",tags=["Authentication"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.") # verifies the email/username
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.") # verifies the password.

    access_token = oauth2.create_access_token(data={"user_id": user.id}) # if the attempted credentials are correct, it will generate an access token
    return {"access_token": access_token, "token_type": "bearer"}