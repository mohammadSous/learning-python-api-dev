from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):  #Validates every field in the Class, and tries to convert first, if the conversion to a set datatype fails it will errors.
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    #rating: int | None = None # # Optional field, accepts an int or None (Union type)

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) #pydantic.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() #grabs all entries from our posts table, same as SELECT * FROM posts;
    return {"data": posts}


@app.get("/posts") # GETS all posts
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() #grabs all entries from our posts table, same as SELECT * FROM posts;
    return posts


# @app.get("/posts/latest")
# def get_latest_post():
#     return {"detail": my_posts[-1]}

@app.get("/posts/{id}") #{id} = path parameter.
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: # clinet supplies an id, if it doesn't exist => error 404. (post not found)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post
    

@app.patch("/posts/{id}")
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):
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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) # fetch
    existing_post = post_query.first() # check if it exists
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    post_query.delete(synchronize_session=False) # delete it 
    db.commit() # save it

    return