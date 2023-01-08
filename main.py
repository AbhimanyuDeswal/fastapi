from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password')
    cursor = conn.cursor()
    print("connected")
except Exception as error:
    print("not connected, error:", error)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    cursor.execute("""insert into posts ( "title", "content", "published") values (%s, %s, %s) returning*""",
    (post.title, post.content, post.published))
    my_posts = cursor.fetchone()
    conn.commit()
    return {"new post":my_posts}

@app.get("/posts")
async def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"all posts":posts}

@app.get("/posts/{id}")
async def get_one_post(id:int):
    cursor.execute("""select * from posts where id=%s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return post

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning*""",
    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"updated_post":updated_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""delete from posts where id=%s returning*""", (str(id)))
    old_post=cursor.fetchall()
    conn.commit()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return status.HTTP_204_NO_CONTENT