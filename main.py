from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel): #Validates/Checks if the title and content are String dataType if not it will throw an error 
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello, World!!!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data": new_post}

#take the data, store it in the db, then fetch it from there.