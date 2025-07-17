import strawberry
from controllers.like_controller import get_likes_info_controller

@strawberry.type
class LikeInfo:
    postId: str
    likesCount: int  

@strawberry.type
class Query:
    @strawberry.field
    def likesCount(self, postId: str) -> LikeInfo: 
        data = get_likes_info_controller(postId)
        return LikeInfo(postId=data["postId"], likesCount=data["likes_count"])

schema = strawberry.Schema(query=Query)
