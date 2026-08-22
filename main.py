from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "fav foods", "content": "i like pizza", "id": 2}]

def find_post(id: int):
    for i in my_posts:
        if i['id'] == id:
            return i

class Post(BaseModel):  #Validates every field in the Class, and tries to convert first, if the conversion to a set datatype fails it will errors.
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    rating: int | None = None # # Optional field, accepts an int or None (Union type)

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump() # model dump turns a pydantic model into a dict.
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # send back the brand new post that we added to our posts.



@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/latest")
def get_latest_post():
    return {"detail": my_posts[-1]}

@app.get("/posts/{id}") #{id} = path parameter.
def get_post(id: int):
    post = find_post(id)
    if not post: # clinet supplies an id, if it doesn't exist > error 404. (post not found)
        raise HTTPException(status_code = 404, detail = f"post with id: {id} was not found")
    return {"post_details": post}
    

@app.put("/posts/{id}")
def update_post():
    pass


@app.delete("/posts/{id}")
def delete_post():
    pass