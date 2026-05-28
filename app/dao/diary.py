from sqlalchemy.orm import Session

from app.models.diary import Diary
from app.schemas.nlp import DiaryCreate


def create_diary(db: Session, diary_in: DiaryCreate) -> Diary:
    """
    사용자 일기 원본 데이터를 DB에 적재
    """
    db_diary = Diary(user_id=diary_in.user_id, content=diary_in.content)
    db.add(db_diary)

    return db_diary
