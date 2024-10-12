from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()  # Create an instance of FastAPI


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
    return {"Data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000)
    my_posts.append(post_dict)
    print("New Post", my_posts)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
def read_post(post_id: int, response: Response):
    for post in my_posts:
        if post["id"] == post_id:
            print("Respose", response)
            return {"Data": post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found any post with the given {post_id}",
    )


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post not found with the given Id {post_id}",
    )


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    for index, existing_post in enumerate(my_posts):
        if existing_post["id"] == post_id:
            my_posts[index] = post.model_dump()
            return {"data": my_posts[index]}
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail=f"Post not found with the given Id {post_id}"
    )
