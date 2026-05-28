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
        self, db: Session, user_id: int, target_date: date
    ) -> dict:
        """
        [R] 💡 핵심 통계 쿼리
        특정 날짜(target_date) 기준 '최근 7일' 동안 누적된 11가지 메트릭의 총합(SUM)을 구합니다.
        """
        # 최근 7일 범위를 계산 (예: 오늘이 5월 26일이면 5월 20일 ~ 5월 26일)
        start_date = target_date - timedelta(days=6)

        # SQLAlchemy func.sum을 활용하여 11개 컬럼을 각각 더해 상용 쿼리 한 방으로 묶음
        result = (
            db.query(
                func.sum(DiaryNlpMetric.burnout_count).label("burnout_count"),
                func.sum(DiaryNlpMetric.sleep_lack_count).label("sleep_lack_count"),
                func.sum(DiaryNlpMetric.insomnia_count).label("insomnia_count"),
                func.sum(DiaryNlpMetric.delivery_count).label("delivery_count"),
                func.sum(DiaryNlpMetric.sedentary_count).label("sedentary_count"),
                func.sum(DiaryNlpMetric.exercise_count).label("exercise_count"),
                func.sum(DiaryNlpMetric.breakfast_skip_count).label(
                    "breakfast_skip_count"
                ),
                func.sum(DiaryNlpMetric.alcohol_count).label("alcohol_count"),
                func.sum(DiaryNlpMetric.msk_pain_count).label("msk_pain_count"),
                func.sum(DiaryNlpMetric.vegetable_count).label("vegetable_count"),
                func.sum(DiaryNlpMetric.regular_meal_count).label("regular_meal_count"),
            )
            .filter(
                DiaryNlpMetric.user_id == user_id,
                DiaryNlpMetric.date.between(
                    start_date, target_date
                ),  # 💡 주입된 비즈니스 date 기준 필터링
            )
            .first()
        )

        # 만약 최근 7일간 쓴 일기가 단 한 장도 없다면 None이 반환되므로 기본값 0 구조로 방어 처리
        if not result or result[0] is None:
            return {field: 0 for field in DiaryNlpMetricResponse.model_fields.keys()}

        # 쿼리 결과를 딕셔너리 형태로 정갈하게 말아서 반환
        return {
            "burnout_count": int(result.burnout_count),
            "sleep_lack_count": int(result.sleep_lack_count),
            "insomnia_count": int(result.insomnia_count),
            "delivery_count": int(result.delivery_count),
            "sedentary_count": int(result.sedentary_count),
            "exercise_count": int(result.exercise_count),
            "breakfast_skip_count": int(result.breakfast_skip_count),
            "alcohol_count": int(result.alcohol_count),
            "msk_pain_count": int(result.msk_pain_count),
            "vegetable_count": int(result.vegetable_count),
            "regular_meal_count": int(result.regular_meal_count),
        }
