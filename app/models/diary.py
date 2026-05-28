from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from app.core.db_connection import EntityBase


class Diary(EntityBase):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
