from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1)  # Validation 활요 가능
    gender: str
    birth_date: date


class UserRead(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    total: int
    users: List[UserRead]


class UserHealthProfileUpdate(BaseModel):
    """
    사용자의 신체 스펙 및 건강 마스터 정보 입력/수정 요청 DTO
    """

    bmi: float | None = Field(None, ge=10.0, le=60.0, description="체질량지수 (BMI)")
    waist_cm: float | None = Field(None, ge=30.0, le=200.0, description="허리둘레 (cm)")
    sbp: int | None = Field(None, ge=50, le=250, description="수축기 혈압 (mmHg)")
    total_cholesterol: int | None = Field(
        None, ge=0, description="총 콜레스테롤 (mg/dL)"
    )
    hdl: int | None = Field(None, ge=0, description="HDL 콜레스테롤 (mg/dL)")
    smoking: str | None = Field(
        None, description="흡연 상태 ('Ex-smoker', 'Never', 'Current' 등)"
    )
    diabetes_history: bool | None = Field(False, description="당뇨 과거력 여부")
    hypertension_medication: bool | None = Field(
        False, description="고혈압 약 복용 여부"
    )
    family_history_cvd: bool | None = Field(False, description="심혈관질환 가족력 여부")
    family_history_dm: bool | None = Field(False, description="당뇨 가족력 여부")

    model_config = ConfigDict(from_attributes=True)
