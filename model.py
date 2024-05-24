from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Poem(Base):
    __tablename__ = "poem"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(256))
    author = Column(String(256))
    dynasty = Column(String(256))
    content = Column(LONGTEXT)
    trans = Column(LONGTEXT)
    annotation = Column(LONGTEXT)
    appreciation = Column(LONGTEXT)
    background = Column(LONGTEXT)
    created_at = Column(DateTime)
