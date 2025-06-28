from sqlalchemy import select, update
from datetime import datetime
from fastapi import HTTPException
from models.like_model import Like
from models.post_model import Post
from models.pet_model import Pet
from config.db import SessionReactions, SessionPost, SessionPet
from utils.webhook_utils import send_like_webhook

def add_like_controller(postId, responsibleId, petId):
    db_reactions = SessionReactions()
    db_posts = SessionPost()
    db_pets = SessionPet()

    try:
        # Verify that the pet you want to like belongs to the person responsible
        pet = db_pets.execute(
            select(Pet).where(
                Pet.id == petId,
                Pet.responsibleId == responsibleId
            )
        ).scalar_one_or_none()

        if not pet:
            raise HTTPException(status_code=403, detail="Responsible does not own the pet trying to like")

        # Verify that the post exists
        post = db_posts.execute(
            select(Post).where(Post.id == postId)
        ).scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

       # Verify that the like does not already exist
        existing_like = db_reactions.execute(
            select(Like).where(
                Like.postId == postId,
                Like.petId == petId
            )
        ).scalar_one_or_none()

        if existing_like:
            raise HTTPException(status_code=400, detail="Like already exists")

       # Insert new like
        new_like = Like(
            postId=postId,
            petId=petId,
            createdAt=datetime.utcnow()
        )
        db_reactions.add(new_like)
        db_reactions.commit()

        ## Increase the like counter on the post
        db_posts.execute(
            update(Post)
            .where(Post.id == postId)
            .values(likes=Post.likes + 1)
        )
        db_posts.commit()

        # WebHook a Notifications   
        payload = {
            "event": "LIKE_ADDED",
            "data": {
                "postId": postId,
                "petId": petId,
                "responsibleId": responsibleId,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        send_like_webhook(payload)

        return {"message": "Like added successfully"}
    


    finally:
        db_reactions.close()
        db_posts.close()
        db_pets.close()
