from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from config.db import Base

class Like(Base):
    __tablename__ = "Likes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    postId = Column(UUID(as_uuid=True))
    petId = Column(UUID(as_uuid=True))
    createdAt = Column(DateTime)
