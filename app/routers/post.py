from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, schemas, oauth
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[schemas.PostOut])
def read_post(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    print("LIMIT", limit)
    posts = (
        db.query(model.Posts, func.count(model.Votes.post_id).label("votes"))
        .join(model.Votes, model.Votes.post_id == model.Posts.id, isouter=True)
        .filter(model.Posts.title.contains(search))
        .group_by(model.Posts.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return [{"Post": post, "votes": votes} for post, votes in posts]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    print("Current User", current_user.id)
    new_post = model.Posts(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostOut)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    post = (
        db.query(model.Posts, func.count(model.Votes.post_id).label("votes"))
        .join(model.Votes, model.Votes.post_id == model.Posts.id, isouter=True)
        .filter(model.Posts.id == post_id)
        .group_by(model.Posts.id)
        .first()
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any post with the given id {post_id}",
        )

    return {"Post": post.Posts, "votes": post.votes}


@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    post_query = db.query(model.Posts).filter(model.Posts.id == post_id)
    post = post_query.first()
    print("POST OWNER ID________________________", post.owner_id)
    print("Current ID________________________", current_user.id)
    if post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    post_query = db.query(model.Posts).filter(model.Posts.id == post_id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
