from sqlalchemy import select
from fastapi import HTTPException
from models.like_model import Like
from models.post_model import Post
from config.redis_client import redis_client
from config.db import SessionReactions, SessionPost
from uuid import UUID

CACHE_TTL = 60

def get_likes_info_controller(postId: UUID):
    db_reactions = SessionReactions()
    db_posts = SessionPost()

    try:
        # Buscar el post
        post = db_posts.execute(
            select(Post).where(Post.id == postId)
        ).scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        cache_key = f"post:{postId}:likes_count"
        cached_likes_count = redis_client.get(cache_key)

        if cached_likes_count is not None:
            like_count = int(cached_likes_count)
        else:
            like_count = post.likes
            redis_client.set(cache_key, like_count, ex=CACHE_TTL)

        likes = db_reactions.execute(
            select(Like).where(Like.postId == postId)
        ).scalars().all()

        likes_list = [
            {
                "likeId": like.id,
                "postId": like.postId,
                "petId": like.petId,
                "createdAt": like.createdAt.isoformat() if like.createdAt else None
            }
            for like in likes
        ]

        return {
            "postId": postId,
            "likes_count": like_count,
            "likes_details": likes_list
        }

    finally:
        db_reactions.close()
        db_posts.close()
