from fastapi import FastAPI
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()  # Create an instance of FastAPI

# model.Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"Message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
