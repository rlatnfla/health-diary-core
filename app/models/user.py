from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.user import UserHealthProfileUpdate

from ..core.db_connection import EntityBase


class User(EntityBase):
    __tablename__ = "users"

    # 사용자 시스템 정보 및 기본 인적사항
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)  # M/F/null
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # health info column
    bmi: Mapped[float | None] = mapped_column(Float)
    waist_cm: Mapped[float | None] = mapped_column(Float)
    sbp: Mapped[int | None] = mapped_column(Integer)  # 수축기 혈압
    total_cholesterol: Mapped[int | None] = mapped_column(Integer)
    hdl: Mapped[int | None] = mapped_column(Integer)
    smoking: Mapped[str | None] = mapped_column(String)  # current/past/never/null
    diabetes_history: Mapped[bool | None] = mapped_column(Boolean, default=False)
    hypertension_medication: Mapped[bool | None] = mapped_column(Boolean, default=False)
    family_history_cvd: Mapped[bool | None] = mapped_column(Boolean, default=False)
    family_history_dm: Mapped[bool | None] = mapped_column(Boolean, default=False)

    def update_health_profile(self, profile_in: "UserHealthProfileUpdate") -> None:
        update_data = profile_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)
