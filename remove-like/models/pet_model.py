from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from config.db import Base

class Pet(Base):
    __tablename__ = "Pets"
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    image = Column(String)
    birthdate = Column(DateTime)
    residence = Column(String)
    gender = Column(String)
    color = Column(String)
    responsibleId = Column(UUID(as_uuid=True))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
