from pydantic import BaseModel

class LikeRequest(BaseModel):
    postId: str
    petId: str

class LikeResponse(BaseModel):
    message: str