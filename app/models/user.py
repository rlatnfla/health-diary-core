from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..core.db_connection import EntityBase

class User(EntityBase):
    __tablename__ = "users"

    # 로그인 관련 정보
    id = Column(Integer, primary_key=True, index=True)

    # 사용자 인적사항 정보
    gender = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)

    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())