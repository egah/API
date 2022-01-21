from fastapi import FastAPI, Response, status, HTTPException
from typing import Dict, Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from typing import Any
#from psycopg2.extras import RealDictCusor
app = FastAPI()
# https://pydantic-docs.helpmanual.io/usage/validators/

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='10.188.228.141', database='fastapi Database',user='epiphane',password='mosesmalone321')
        cusor = conn.cursor()
        print('connection successfully established')
        break
    except Exception as error:
        print('connection error: %s' % error)
        time.sleep(3)

my_post_array = [{"title":"Vanitifer","content":"Livre is about","rating":4,"id":0},
        {"title":"New yorker","content":"Serena","published":False,"rating":0,"id":1}]

def find_post(id):
    for p in my_post_array:
        if p["id"] == id:
            return p
def find_index(id):
    id = int(id)
    for indice, post in enumerate(my_post_array,0):
        if post['id'] == id:
            return indice

#PATH OPERATION OR ROOT IN ODER WEB FRAMEWORK AND LANGUAGE
@app.get("/login")
def root():
    return {"message": "Hello World :::"}

@app.get('/posts')
def get_post():
    cusor.execute("SELECT * from posts")
    data = cusor.fetchall()
    return {'data':data}

#def create_post(Payload: Dict = Body(...)):
@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cusor.execute("""INSERT INTO posts (title, content,
    published, rating) VALUES (%s,%s,%s,%s)""",
    (post.title,post.content,post.published,post.rating))
    new_post = cusor.fetchone()
    conn.commit()
    return {'data':new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f" post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id : {id} not found")
    return {'post_detail':post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    indice = find_index(id)
    if indice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    my_post_array.pop(indice)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    indice = find_index(id)
    if indice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    post_doc = post.dict()
    post_doc['id'] = id
    my_post_array[indice] = post_doc
    return {"data":my_post_array}
