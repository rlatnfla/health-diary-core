from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.diary_nlp_metrics import DiaryNlpMetric
from app.schemas.diary_analysis import DiaryNlpMetricResponse


class DiaryNlpMetricDao:
    def create_nlp_metrics(
        self,
        db: Session,
        user_id: int,
        diary_id: int,
        diary_date: date,
        metrics_in: DiaryNlpMetricResponse,
    ) -> DiaryNlpMetric:
        """
        NLP 서버의 분석 결과(0 또는 1)를 유저 및 일기 매핑 정보와 함께 저장합니다.
        """
        db_nlp_metric = DiaryNlpMetric(
            user_id=user_id,
            diary_id=diary_id,
            date=diary_date,
            **metrics_in.model_dump(),
        )
        db.add(db_nlp_metric)
        return db_nlp_metric

    def get_weekly_aggregated_metrics(
        self,
        db: Session,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> dict:
        """
        지정된 기간(7일) 동안 해당 유저가 기록한 11가지 메트릭의 각각의 총합(SUM)을 계산합니다.
        """
        # 집계 대상이 되는 11가지 메트릭 필드 리스트 정의
        metric_columns = [
            "burnout_count",
            "sleep_lack_count",
            "insomnia_count",
            "delivery_count",
            "sedentary_count",
            "exercise_count",
            "alcohol_count",
            "msk_pain_count",
            "vegetable_count",
            "caffeine_count",
            "regular_meal_count",
        ]

        # 쿼리에 넣을 func.sum(컬럼) 표현식들을 동적으로 생성
        # 예: func.sum(DiaryNlpMetric.burnout_count).label("burnout_count")
        sum_expressions = [
            func.sum(getattr(DiaryNlpMetric, col)).label(col) for col in metric_columns
        ]

        # 데이터베이스 단일 쿼리 실행 (조건: 특정 유저 ID & 날짜 범위)
        result = (
            db.query(*sum_expressions)
            .filter(
                DiaryNlpMetric.user_id == user_id,
                DiaryNlpMetric.date >= start_date,
                DiaryNlpMetric.date <= end_date,
            )
            .first()
        )

        # 만약 해당 기간에 작성된 일기가 하나도 없다면 모든 결과값이 None으로 나옵니다.
        # 서비스 레이어(DTO 부품)에서 안전하게 연산할 수 있도록 None 일 경우 0으로 보정하여 딕셔너리로 반환합니다.
        if not result or result[0] is None:
            return {col: 0 for col in metric_columns}

        # 쿼리 결과를 Key-Value 형태의 딕셔너리로 마샬링하여 반환
        return result._asdict()
