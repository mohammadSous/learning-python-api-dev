from .. import models, schemas
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter()


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) #pydantic.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/")
async def root():
    return {"message": "Hello, World!"}


@router.get("/posts", response_model=List[schemas.Post]) # GETS all posts
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() #grabs all entries from our posts table, same as SELECT * FROM posts;
    return posts


@router.get("/posts/{id}", response_model= schemas.Post) #{id} = path parameter.
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: # clinet supplies an id, if it doesn't exist => error 404. (post not found)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@router.patch("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # grabs the post by it id, but does nothing yet.
    existing_post = post_query.first()  # runs the query once to check if the post exist or not.

    if existing_post is None:  # same 404 check.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    # .update() runs the actual UPDATE on whatever post_query's WHERE clause matches
    # post.model_dump(exclude_unset=True) = only the fields the client actually sent, as a dict
    # synchronize_session=False = required for bulk .update(), skips SQLAlchemy's normal object-syncing

    db.commit()  # same role as conn.commit() nothing saves until this runs

    return post_query.first() # re-run the query to return the UPDATED row, not the stale one


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) # fetch
    existing_post = post_query.first() # check if it exists
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    post_query.delete(synchronize_session=False) # delete it 
    db.commit() # save it

    return