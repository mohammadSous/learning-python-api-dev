from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "fav foods", "content": "i like pizza", "id": 2}]

class Post(BaseModel): #Validates/Checks if the title and content are String dataType if not it will throw an error 
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    rating: int | None = None # XOR operation. only takes an int or nothing.

@app.get("/")
async def root():
    return {"message": "Hello, World!!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump # model dump turns a pydantic model into a dict.
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # send back the brand new post that we added to our posts.

#take the data, store it in the db, then fetch it from there.