from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, func

from app.core.db_connection import EntityBase


class DiaryNlpMetric(EntityBase):
    __tablename__ = "diary_nlp_metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    diary_id = Column(
        Integer,
        ForeignKey("diaries.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    date = Column(Date, nullable=False, index=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)

    burnout_count = Column(Integer, default=0, nullable=False)
    sleep_lack_count = Column(Integer, default=0, nullable=False)
    insomnia_count = Column(Integer, default=0, nullable=False)
    delivery_count = Column(Integer, default=0, nullable=False)
    sedentary_count = Column(Integer, default=0, nullable=False)
    exercise_count = Column(Integer, default=0, nullable=False)
    breakfast_skip_count = Column(Integer, default=0, nullable=False)
    alcohol_count = Column(Integer, default=0, nullable=False)
    msk_pain_count = Column(Integer, default=0, nullable=False)
    vegetable_count = Column(Integer, default=0, nullable=False)
    regular_meal_count = Column(Integer, default=0, nullable=False)
