from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from schemas.like_schema import LikeRequest, LikeResponse
from controllers.like_controller import remove_like_controller
from middlewares.auth_middleware import get_current_responsible

router = APIRouter()

# Security scheme to show the lock icon in Swagger
security_scheme = HTTPBearer()

@router.delete(
    "/likes/remove",
    tags=["Likes"],
    summary="Remove Like from post",
    description="""
Allows removing a Like previously added by a pet.  
""",
    response_model=LikeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Like removed successfully",
            "content": {
                "application/json": {
                    "schema": LikeResponse.model_json_schema()
                }
            }
        },
        404: {"description": "Like or post not found"},
        403: {"description": "Responsible does not own the pet"},
        401: {"description": "Token missing or invalid"},
    },
    dependencies=[Depends(security_scheme)],
)
def remove_like(
    request_data: LikeRequest,
    responsible_id: str = Depends(get_current_responsible)
):
    """
    - The JWT is extracted and validated via get_current_responsible.
    - Returns 401 if the token is invalid.
    - Returns 403 if the pet does not belong to the authenticated responsible.
    - Returns 404 if the like does not exist.
    """
    return remove_like_controller(
        request_data.postId,
        responsible_id,
        request_data.petId
    )
