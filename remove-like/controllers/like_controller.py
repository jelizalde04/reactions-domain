from sqlalchemy import select, update, delete
from fastapi import HTTPException
from models.like_model import Like
from models.post_model import Post
from models.pet_model import Pet
from config.db import SessionReactions, SessionPost, SessionPet

def remove_like_controller(postId, responsibleId, petId):
    db_reactions = SessionReactions()
    db_posts = SessionPost()
    db_pets = SessionPet()

    try:
       
        pet = db_pets.execute(
            select(Pet).where(
                Pet.id == petId,
                Pet.responsibleId == responsibleId
            )
        ).scalar_one_or_none()

        if not pet:
            raise HTTPException(status_code=403, detail="Responsible does not own the pet trying to remove like")


        post = db_posts.execute(
            select(Post).where(Post.id == postId)
        ).scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        existing_like = db_reactions.execute(
            select(Like).where(
                Like.postId == postId,
                Like.petId == petId
            )
        ).scalar_one_or_none()

        if not existing_like:
            raise HTTPException(status_code=404, detail="Like does not exist")

        db_reactions.execute(
            delete(Like).where(
                Like.postId == postId,
                Like.petId == petId
            )
        )
        db_reactions.commit()

        new_likes_count = max(post.likes - 1, 0)
        db_posts.execute(
            update(Post)
            .where(Post.id == postId)
            .values(likes=new_likes_count)
        )
        db_posts.commit()

        return {"message": "Like removed successfully"}

    finally:
        db_reactions.close()
        db_posts.close()
        db_pets.close()
