from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base

class User(Base):

    __tablename__ = "user"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True
    )

    password = Column(
        String(255)
    )

    email = Column(
        String(100)
    )

    create_time = Column(
        DateTime,
        server_default=func.now()
    )