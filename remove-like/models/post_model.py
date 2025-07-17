from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from config.db import Base

class Post(Base):
    __tablename__ = "Posts"
    id = Column(UUID(as_uuid=True), primary_key=True)
    petId = Column(UUID(as_uuid=True))
    content = Column(String)
    image = Column(String)
    likes = Column(Integer)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
