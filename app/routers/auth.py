from .. import models, schemas, utils
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter(prefix= "/login",tags=["Authentication"])


router.post("/", status_code=status.HTTP_201_CREATED)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Credentials.")
    if not utils.verify(user_credentials.password, models.User.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Invalid Credentials.")

    return {"Example": "TOKEN"}