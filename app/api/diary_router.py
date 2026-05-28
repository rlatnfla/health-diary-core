from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db_connection import get_db_session
from app.schemas.nlp import DiaryCreate
from app.services.diary_service import DiaryService
from app.services.nlp.nlp_base import NlpClientBase
from app.services.nlp.nlp_http import HttpNlpClient
from app.services.user_service import UserService

router = APIRouter(prefix="/diaries", tags=["Diaries"])


# 원하는 구현체 리턴
def _get_nlp_client() -> NlpClientBase:
    return HttpNlpClient(nlp_server_url="http://localhost:8001")


def _get_diary_service(
    db: Session = Depends(get_db_session),
    nlp_client: NlpClientBase = Depends(_get_nlp_client),
) -> DiaryService:
    return DiaryService(db, nlp_client)


def _get_user_service(db: Session = Depends(get_db_session)) -> UserService:
    return UserService(db)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_and_process_diary(
    diary_in: DiaryCreate,
    diary_service: DiaryService = Depends(_get_diary_service),
    user_service: UserService = Depends(_get_user_service),
):
    # 1. 사용자 존재 여부 확인 (read only 트랜잭션 점유)
    await user_service.validate_user_exists(diary_in.user_id)

    # 2. nlp 서버로의 통신 (트랜잭션 비점유)
    nlp_result = await diary_service.analyze_today_lifestyle(diary_in.content)

    # 3. Diary 및 metrics? 를 같은 트랜잭션 단위에서 영속화 (둘다 commit, or 둘다 rollback 되게끔)
    await diary_service.save_diary_with_metrics(diary_in.user_id, diary_in, nlp_result)

    return nlp_result
