from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

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
    return {"data": "This is your posts"}

@app.post("/posts")
def create_posts(post: Post):
    print(post.model_dump()) #you can use either this or just new_post but, new_post is a pydantic model type, this .model_dump() turns it into a python dict
    return {"data": post}

#take the data, store it in the db, then fetch it from there.