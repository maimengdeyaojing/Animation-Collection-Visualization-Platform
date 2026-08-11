from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Text

from app.database import Base


class AnimeCollection(Base):

    __tablename__ = "anime_collection"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))

    date = Column(Date)

    year = Column(Integer)

    month = Column(Integer)

    image_url = Column(Text)

    status = Column(Integer)