from sqlalchemy import Column, Float, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Avatar(Base):
    __tablename__ = 'avatar_data'
    id = Column(Integer, Sequence('avatar_id_seq'), primary_key=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    note = Column(String(50), nullable=True)
    bmi = Column(Float, nullable=True)

#comment로 쓰니까, oracle에서 comment는 예약어라서, 컬럼명이 얘만 소문자로 나와서 그걸 피하기 위해서이다.