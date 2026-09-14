from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class Reports(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_text = Column(Text, nullable=True)
    result = Column(Text, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()