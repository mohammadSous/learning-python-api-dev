from .. import models, schemas, utils
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix= "/vote", tags= ["Vote"])


@router.post("/", status_code= status.HTTP_201_CREATED)
def vote():
    