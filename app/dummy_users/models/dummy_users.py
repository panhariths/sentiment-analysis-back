from sqlalchemy import Column, Unicode, Integer
from datastores.database.base import Base


# User model inherits from BaseModel
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=True)
