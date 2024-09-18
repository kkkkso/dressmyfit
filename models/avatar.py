from sqlalchemy import Column, Float, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Avatar(Base):
    __tablename__ = 'avatar_data'
    id = Column(Integer, Sequence('avatar_id_seq'), primary_key=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    bmi = Column(Float, nullable=True)