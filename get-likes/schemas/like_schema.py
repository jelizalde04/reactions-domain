from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class LikeDetail(BaseModel):
    likeId: UUID
    postId: UUID
    petId: UUID
    createdAt: Optional[datetime]

    class Config:
        orm_mode = True

class LikeListResponse(BaseModel):
    postId: UUID
    likes_count: int
    likes_details: List[LikeDetail]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "998e719c-848c-4f60-9ff2-8d86a0a9616c",
                "likes_count": 5,
                "likes_details": [
                    {
                        "likeId": "a62731bf-1148-48d7-aa29-9e7c4667be87",
                        "postId": "998e719c-848c-4f60-9ff2-8d86a0a9616c",
                        "petId": "b35beaad-f5fd-4a77-bf68-9dbca72b36f2",
                        "createdAt": "2025-06-27T10:30:00"
                    }
                ]
            }
        }
