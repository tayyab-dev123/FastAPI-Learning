from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()  # Create an instance of FastAPI


def get_db_connection():
    while True:
        try:
            conn = psycopg.connect(
                "host=localhost password=tayyab dbname=fastapi user=postgres",
                row_factory=dict_row,
            )
            print("Connection successful")
            return conn
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool
    rating: Optional[int] = None


my_posts = [
    {"id": 1, "title": "Hello World", "content": "This is my first blog post"},
    {"id": 2, "title": "Second Post", "content": "This is my second blog post"},
]


@app.get("/")  # Decorator to define the path of the endpoint
def read_root():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM posts""")
        posts = cur.fetchall()
        print("All Posts", posts)
        return {"Data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
            (post.title, post.content, post.published),
        )
        new_Post = cur.fetchone()
        conn.commit()
        return {"data": new_Post}


@app.get("/posts/{post_id}")
def read_post(post_id: int, response: Response):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM posts WHERE id = %s """, (post_id,))
        post = cur.fetchone()
        print(post)
        conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any post with the given {post_id}",
        )
    return {"Data": post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
        deleted_post = cur.fetchone()
        print("deleted_post", deleted_post)
        conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # for index, post in enumerate(my_posts):
    #     if post["id"] == post_id:
    #         my_posts.pop(index)
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """UPDATE posts set title= %s , content= %s , published= %s where id = %s RETURNING *""",
            (post.title, post.content, post.published, post_id),
        )
        updated_post = cur.fetchone()
        print("updated_post", updated_post)
        conn.commit()
    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    return {"data": updated_post}
