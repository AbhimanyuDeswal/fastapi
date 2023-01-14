from fastapi import FastAPI, Depends
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/", )
async def root(db: Session=Depends(get_db)):
    return {"message": "Hello World"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post, db:Session=Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"new post":new_post}

@app.get("/posts")
async def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"all posts":posts}

@app.get("/posts/{id}")
async def get_one_post(id:int, db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return post

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"updated_post":post_query.first()}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_204_NO_CONTENT