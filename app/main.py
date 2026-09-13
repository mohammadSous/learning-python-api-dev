from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from typing import List


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) #pydantic.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/posts", response_model=List[schemas.Post]) # GETS all posts
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() #grabs all entries from our posts table, same as SELECT * FROM posts;
    return posts


# @app.get("/posts/latest")
# def get_latest_post():
#     return {"detail": my_posts[-1]}


@app.get("/posts/{id}", response_model= schemas.Post) #{id} = path parameter.
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: # clinet supplies an id, if it doesn't exist => error 404. (post not found)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@app.patch("/posts/{id}", response_model= schemas.Post)
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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) # fetch
    existing_post = post_query.first() # check if it exists
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    post_query.delete(synchronize_session=False) # delete it 
    db.commit() # save it

    return


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with ID: {id} does not exist.")
    
    return user