from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.decorators import transactional
from app.dao import user as user_dao
from app.dao.diary_nlp_metrics import DiaryNlpMetricDao
from app.exceptions.base_exception import ResourceNotFoundException
from app.schemas.weekly_report import (
    ModelAnalysisResult,
    WeeklyNlpPayload,
    WeeklyReportAnalyzer,
)
from app.services.nlp.nlp_base import NlpClientBase


class WeeklyReportService:
    def __init__(self, db: Session, nlp_client: NlpClientBase):
        self.db = db
        self.diary_metric_dao = DiaryNlpMetricDao()
        self.nlp_client = nlp_client

    @transactional(read_only=True)
    async def prepare_weekly_nlp_payload(
        self, user_id: int, target_date: date, model_result: ModelAnalysisResult
    ) -> WeeklyNlpPayload:
        # 1. 일주일(7일) 날짜 범위 계산
        start_date = target_date - timedelta(days=6)
        end_date = target_date

        # 2. User 테이블에서 헬스 인포 컬럼 정보 조회
        db_user = user_dao.get_user_by_id(self.db, user_id)
        if db_user is None:
            raise ResourceNotFoundException("사용자")

        # 3. 7일간의 메트릭 조회
        metrics_sum = self.diary_metric_dao.get_weekly_aggregated_metrics(
            self.db, user_id, start_date, end_date
        )

        # 4. 수집된 모든 영속성 데이터를 WeeklyNlpPayload DTO 규격으로 바인딩 (마샬링)
        payload = WeeklyNlpPayload(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            # 일기 메트릭 합산본
            **metrics_sum,
            # User 엔티티의 health info column을 누수 없이 그대로 이식
            gender=db_user.gender,
            birth_date=db_user.birth_date,
            bmi=db_user.bmi,
            waist_cm=db_user.waist_cm,
            sbp=db_user.sbp,
            total_cholesterol=db_user.total_cholesterol,
            hdl=db_user.hdl,
            smoking=db_user.smoking,
            diabetes_history=db_user.diabetes_history,
            hypertension_medication=db_user.hypertension_medication,
            family_history_cvd=db_user.family_history_cvd,
            family_history_dm=db_user.family_history_dm,
            # 분석 모델 추상화 결과 주입
            model_result=model_result,
        )
        return payload

    # 🔥 [메서드 2] NLP 서버 요청 전송 메서드
    # 이 메서드는 순수하게 외부망 인터넷 통신(HTTP I/O BOUND)만 담당합니다.
    # 내부에서 어떠한 DB 트랜잭션도 참조하지 않으므로 무겁게 커넥션을 쥐고 있을 일이 전혀 없습니다.
    async def send_to_nlp_server(
        self, payload: WeeklyNlpPayload, analyzer: WeeklyReportAnalyzer
    ) -> str:
        # 주입받은 analyzer 인터페이스를 활용해 통신 수행 (동적 다형성 활용)
        report_result_text = await analyzer.analyze_weekly_health(payload)
        return report_result_text
