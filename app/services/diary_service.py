from sqlalchemy.orm import Session

from app.core.decorators import transactional
from app.dao import diary as diary_dao
from app.dao.diary_nlp_metrics import DiaryNlpMetricDao
from app.schemas.diary_analysis import DiaryNlpMetricResponse
from app.schemas.nlp import DiaryCreate
from app.services.nlp.nlp_base import NlpAnalysisRequestSchema, NlpClientBase
from app.services.user_service import UserService


class DiaryService:
    """
    일기 도메인의 비즈니스 시나리오 총괄 레이어
    """

    def __init__(self, db: Session, nlp_client: NlpClientBase):
        self.db = db
        self.nlp_client = nlp_client
        self.user_service = UserService(db)
        self.metric_dao = DiaryNlpMetricDao()

    async def analyze_today_lifestyle(self, content: str) -> DiaryNlpMetricResponse:
        """
        nlp 서버로의 일기 분석 요청
        """
        request_data = NlpAnalysisRequestSchema(content=content)
        raw_response = await self.nlp_client.send_analysis_request(request_data)

        # 엔티티로 매핑해서 리턴
        return DiaryNlpMetricResponse.model_validate(raw_response)

    @transactional()
    async def save_diary_with_metrics(
        self, user_id: int, diary_in: DiaryCreate, metrics_in: DiaryNlpMetricResponse
    ) -> None:
        # 일기 저장 및 id 할당을 위한 flush()
        db_diary = diary_dao.create_diary(self.db, diary_in)
        self.db.flush()

        # DiaryNlpMetric 저장
        self.metric_dao.create_nlp_metrics(
            self.db, user_id, db_diary.id, diary_in.date, metrics_in
        )
