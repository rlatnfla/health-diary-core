from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db_connection import get_db_session
from app.schemas.weekly_report import ModelAnalysisResult, WeeklyReportCreateRequest
from app.services.nlp.nlp_base import NlpClientBase
from app.services.nlp.nlp_http import HttpNlpClient
from app.services.weekly_report_service import WeeklyReportService

router = APIRouter(prefix="/reports", tags=["weekly-report"])

NLP_SERVER_URL = "http://localhost:8000"


def _get_nlp_client() -> NlpClientBase:
    return HttpNlpClient(nlp_server_url=NLP_SERVER_URL)


def _get_weekly_report_service(
    db: Session = Depends(get_db_session),
) -> WeeklyReportService:
    return WeeklyReportService(db, _get_nlp_client)


@router.post("/weekly", status_code=status.HTTP_200_OK)
async def create_weekly_report(
    weekly_report_in: WeeklyReportCreateRequest,
    nlp_client: NlpClientBase = Depends(_get_nlp_client),
    weekly_report_service: WeeklyReportService = Depends(_get_weekly_report_service),
):
    """
    사용자의 일주일치 건강 데이터 및 일기 메트릭을 취합하여 AI 종합 진단 레포트를 생성합니다.
    (의존성 주입을 통한 결합도 최소화 및 트랜잭션 분리 오케스트레이션)
    """

    # 1. TODO: 분석 모델 통신
    mock_model_result = None

    # 2. 페이로드 생성
    nlp_payload = await weekly_report_service.prepare_weekly_nlp_payload(
        user_id=weekly_report_in.user_id,
        target_date=weekly_report_in.target_date,
        model_result=mock_model_result,
    )

    # 3. nlp 통신
    final_report_response = await weekly_report_service.send_to_nlp_server(
        payload=nlp_payload
    )

    return {
        "status": "SUCCESS",
        "message": "주간 건강 위험도 분석 보고서가 성공적으로 발급되었습니다.",
        "data": final_report_response,
    }
