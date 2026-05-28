from pydantic import BaseModel, Field


class DiaryNlpMetricResponse(BaseModel):
    """
    외부 NLP 서버로부터 수신한 오늘 하루의 11가지 라이프스타일 및 행동 분석 결과 DTO.
    각 지표는 오늘 일기에서 해당 내용이 감지되었는지에 따라 0 또는 1의 값을 가집니다.
    """

    burnout_count: int = Field(
        0,
        description="심한 스트레스, 무기력, 번아웃, 과도한 피로감 호소 여부 (0 또는 1)",
    )
    sleep_lack_count: int = Field(
        0, description="늦게 잠, 밤샘, 절대적인 수면 시간 부족 언급 여부 (0 또는 1)"
    )
    insomnia_count: int = Field(
        0, description="잠이 잘 안 남, 중간에 깸, 불면 증상 호소 여부 (0 또는 1)"
    )
    delivery_count: int = Field(
        0, description="배달음식, 야식, 인스턴트, 자극적인 외식 섭취 여부 (0 또는 1)"
    )
    sedentary_count: int = Field(
        0,
        description="하루 종일 누워있음, 오래 앉아서 일만 함 등 신체활동 부족 여부 (0 또는 1)",
    )
    exercise_count: int = Field(
        0, description="헬스, 산책, 조깅 등 의도적인 운동 수행 언급 여부 (0 또는 1)"
    )
    breakfast_skip_count: int = Field(
        0, description="아침 식사 결식, 아점을 먹음 등 아침 거름 여부 (0 또는 1)"
    )
    alcohol_count: int = Field(
        0, description="술을 마심, 맥주 한 잔, 회식 등 음주 행위 여부 (0 또는 1)"
    )
    msk_pain_count: int = Field(
        0,
        description="목, 어깨, 허리, 손목 등 근골격계 통증 이나 결림 호소 여부 (0 또는 1)",
    )
    vegetable_count: int = Field(
        0, description="샐러드, 야채, 채소, 과일, 건강식 챙겨 먹음 언급 여부 (0 또는 1)"
    )
    regular_meal_count: int = Field(
        0, description="제시간에 삼시세끼 규칙적인 식사 완수 여부 (0 또는 1)"
    )

    class Config:
        from_attributes = (
            True  # SQLAlchemy 모델 객체 변환 지원 (혹시 모를 대동을 위해 세팅)
        )
