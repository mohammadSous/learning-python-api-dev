from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "fav foods", "content": "i like pizza", "id": 2}]

# def find_post(id: int): #returns the post by it ID
#     for i in my_posts:
#         if i['id'] == id:
#             return i
        
# def get_post_index(id: int): #returns the post index by it ID
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

class Post(BaseModel):  #Validates every field in the Class, and tries to convert first, if the conversion to a set datatype fails it will errors.
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    #rating: int | None = None # # Optional field, accepts an int or None (Union type)

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi_project', user = 'postgres', password = 'postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("connection to database failed.")
        print(f"Error: {error}")
        time.sleep(2)



@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post): #pydantic
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                   (post.title, post.content, post.published)) #SQL injection proof.
    new_post = cursor.fetchone()
    conn.commit() # Save it to the database.
    return {"data": new_post} # send back the brand new post that we added to our posts.

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""") # runs the SQL command.
    posts = cursor.fetchall() # retrive all posts.
    return {"data": posts}

# @app.get("/posts/latest")
# def get_latest_post():
#     return {"detail": my_posts[-1]}

@app.get("/posts/{id}") #{id} = path parameter.
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""",(str(id),))
    post = cursor.fetchone()
    print(post)
    if not post: # clinet supplies an id, if it doesn't exist => error 404. (post not found)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_details": post}
    

@app.patch("/posts/{id}")
def update_post(id: int, post: PostUpdate):
    cursor.execute("""
        UPDATE posts
        SET title = COALESCE(%s, title),
            content = COALESCE(%s, content),
            published = COALESCE(%s, published)
        WHERE id = %s RETURNING *
        """, (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")

    return