from .. import models, schemas, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List


router = APIRouter(prefix= "/posts", tags= ["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)): # get_current_user ensures they're logged in before making a post
    new_post = models.Post(owner_id= current_user.id, **post.model_dump()) # owner_id is the name of the foreign key in the posts table. **posts... is pydantic validation.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/")
# async def root():
#     return {"message": "Hello, World!"}


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit).offset(skip).all()
        
    return posts


@router.get("/{id}", response_model= schemas.Post) #{id} = path parameter.
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: # clinet supplies an id, if it doesn't exist => error 404. (post not found)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@router.patch("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # grabs the post by it id, but does nothing yet.
    existing_post = post_query.first()  # runs the query once to check if the post exist or not.

    if existing_post is None:  # same 404 check.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id: # check posts/DELETE for if statement details.
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not Autharized to Perfom Request Action.")

    post_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    # .update() runs the actual UPDATE on whatever post_query's WHERE clause matches
    # post.model_dump(exclude_unset=True) = only the fields the client actually sent, as a dict
    # synchronize_session=False = required for bulk .update(), skips SQLAlchemy's normal object-syncing

    db.commit()  # same role as conn.commit() nothing saves until this runs

    return post_query.first() # re-run the query to return the UPDATED row, not the stale one


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) # fetch
    existing_post = post_query.first() # check if it exists
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    
    if existing_post.owner_id != current_user.id: # Check if the user who is attempting to delete this existing post have the same id (owner id) of the person who published that post!
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not Autharized to Perfom Request Action.")

    post_query.delete(synchronize_session=False) # delete it 
    db.commit() # save it

    return