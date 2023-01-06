from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"1", "content":"1", "id":1},{"title":"2", "content":"2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    id = len(my_posts)+1
    new_post = post.dict()
    new_post["id"] = id
    my_posts.append(new_post)
    return {"all post": my_posts}

@app.get("/posts")
async def posts():
    return my_posts

@app.get("/posts/{id}")
async def get_one_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return post