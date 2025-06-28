from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from schemas.like_schema import LikeRequest, LikeResponse
from controllers.like_controller import add_like_controller
from middlewares.auth_middleware import get_current_responsible

router = APIRouter()


security_scheme = HTTPBearer()

@router.post(
    "/likes/add",
    tags=["Likes"],
    summary="Añadir Like a publicación",
    description="""
Permite registrar un Like.
- """,
    response_model=LikeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Like agregado",
            "content": {
                "application/json": {
                    "schema": LikeResponse.model_json_schema()
                }
            }
        },
        400: {"description": "Like ya existe"},
        403: {"description": "Responsible does not own the pet"},
        404: {"description": "Publicación no encontrada"},
        401: {"description": "Token missing or invalid"},
    },
    dependencies=[Depends(security_scheme)],
)
def add_like(
    request_data: LikeRequest,
    responsible_id: str = Depends(get_current_responsible)
):
    """
    - El JWT se extrae y valida desde get_current_responsible.
    - Devuelve 401 si el token es inválido.
    - Devuelve 403 si la mascota no pertenece al responsable autenticado.
    """
    return add_like_controller(
        request_data.postId,
        responsible_id,
        request_data.petId
    )
