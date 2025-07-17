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
        # Verify that the pet belongs to the responsible user
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

        # Check if the like already exists
        existing_like = db_reactions.execute(
            select(Like).where(
                Like.postId == postId,
                Like.petId == petId
            )
        ).scalar_one_or_none()

        if existing_like:
            raise HTTPException(status_code=400, detail="Like already exists")

        # Prepare the new like (do not commit yet)
        new_like = Like(
            postId=postId,
            petId=petId,
            createdAt=datetime.utcnow()
        )
        db_reactions.add(new_like)

        # Get the name of the pet who gave the like
        liker_pet_name = pet.name

        # Get the pet who owns the post
        post_owner_pet = db_pets.execute(
            select(Pet).where(Pet.id == post.petId)
        ).scalar_one_or_none()

        if not post_owner_pet:
            raise HTTPException(status_code=404, detail="Owner pet not found")

        post_owner_pet_name = post_owner_pet.name
        post_owner_responsible_id = post_owner_pet.responsibleId

        # Build the webhook payload
        payload = {
            "event": "LIKE_ADDED",
            "data": {
                "type": "Likes",
                "actorId": str(petId),
                "recipientId": str(postId),
                "responsibleId": str(post_owner_responsible_id),
                "timestamp": datetime.utcnow().isoformat(),
                "content": f"{liker_pet_name} le dio like a una publicación de {post_owner_pet_name}."
            }
        }

        # Try to send the webhook before committing the like
        try:
            send_like_webhook(payload)
        except Exception as e:
            db_reactions.rollback()  # Rollback the like if webhook fails
            raise HTTPException(status_code=500, detail=f"Failed to send like notification: {str(e)}")

        # Commit the like only if webhook was successful
        db_reactions.commit()

        # Update the like counter in the post
        db_posts.execute(
            update(Post)
            .where(Post.id == postId)
            .values(likes=Post.likes + 1)
        )
        db_posts.commit()

        return {"message": "Like added successfully"}

    finally:
        db_reactions.close()
        db_posts.close()
        db_pets.close()
