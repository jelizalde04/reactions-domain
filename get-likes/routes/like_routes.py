from fastapi import APIRouter, status
from fastapi.security import HTTPBearer
from schemas.like_schema import LikeListResponse
from controllers.like_controller import get_likes_info_controller

router = APIRouter()


security_scheme = HTTPBearer()

@router.get(
    "/likes/{postId}",
    tags=["Likes"],
    summary="Retrieve likes for a post",
    description="""
    Retrieves the current number of likes for a specific post,  
    along with the details of all Like records for that post.
    """,
    response_model=LikeListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Likes retrieved successfully"},
        404: {"description": "Post not found"},
        401: {"description": "Token missing or invalid"},
    },

)
def get_likes_info(postId: str):
    """
    Returns:
    - Total number of likes stored in the Post table.
    - List of all Like records associated with the given postId.
    """
    return get_likes_info_controller(postId)
