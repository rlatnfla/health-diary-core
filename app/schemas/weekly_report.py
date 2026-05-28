from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from pydantic import BaseModel


# 1. 앱 클라이언트가 Core 서버로 주간 레포트 생성을 요청하는 규격
class WeeklyReportCreateRequest(BaseModel):
    user_id: int
    target_date: date  # 주간(7일) 범위를 산출하기 위한 기준일


# 2. 분석 모델 결과를 격리/추상화하기 위한 서브 스키마(미정)
class ModelAnalysisResult(BaseModel):
    status: str = "PENDING"
    raw_score: Optional[float] = 0.0


# 3. NLP 서버로 발송할 최종 패키지 규격
class WeeklyNlpPayload(BaseModel):
    user_id: int
    start_date: date
    end_date: date

    # diary_metrics
    burnout_count: int
    sleep_lack_count: int
    insomnia_count: int
    delivery_count: int
    sedentary_count: int
    exercise_count: int
    alcohol_count: int
    msk_pain_count: int
    vegetable_count: int
    caffeine_count: int
    regular_meal_count: int

    # 사용자 기초 정보 및 계측/가족력 데이터
    gender: Optional[str] = None
    birth_date: date
    bmi: Optional[float] = None
    waist_cm: Optional[float] = None
    sbp: Optional[int] = None
    total_cholesterol: Optional[int] = None
    hdl: Optional[int] = None
    smoking: Optional[str] = None
    diabetes_history: Optional[bool] = False
    hypertension_medication: Optional[bool] = False
    family_history_cvd: Optional[bool] = False
    family_history_dm: Optional[bool] = False

    # 분석 모델 결과 추상체 인터페이스 격리
    model_result: ModelAnalysisResult

    # ─── [추상화] 분석 통신 인터페이스 ───


# 데이터 분석 모델이 아직 미정이므로, 나중에 어떤 식으로 완성되든
# 이 서비스 레이어의 흐름이 깨지지 않도록 추상화 장치를 둡니다.
class WeeklyReportAnalyzer(ABC):
    @abstractmethod
    async def analyze_weekly_health(self, payload: WeeklyNlpPayload) -> str:
        pass


# [추상화 구현체] 현재 분석 모델 부재로 인한 작업 중단을 막아줄 Mock 엔진
class MockReportAnalyzer(WeeklyReportAnalyzer):
    async def analyze_weekly_health(self, payload: WeeklyNlpPayload) -> str:
        # 실제 외부 NLP 서버나 분석 엔진으로 HTTP POST 쏘는 로직이 들어갈 자리입니다.
        # 지금은 기능 검증을 위해 딜레이 후 임시 문장을 반환합니다.
        import asyncio

        await asyncio.sleep(0.5)  # 네트워크 지연 시뮬레이션
        return f"유저 {payload.user_id}님의 주간 맞춤형 AI 종합 건강 레포트 발급이 완료되었습니다."
