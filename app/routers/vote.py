from fastapi import APIRouter, Response, Depends, HTTPException, status
from .. import schemas, database, oauth, model
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["VOTE"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    post = db.query(model.Posts).filter(model.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    vote_query = db.query(model.Votes).filter(
        model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id
    )
    vote_found = vote_query.first()

    if vote.dir == 1:
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vote already exists for {current_user.id}",
            )
        new_vote = model.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not vote_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exists",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
