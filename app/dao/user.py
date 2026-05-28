from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


# 사용자 생성
def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        name=user_in.name, gender=user_in.gender, birth_date=user_in.birth_date
    )

    db.add(db_user)
    db.flush()
    return db_user


# 사용자 단건 조회
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


# 사용자 존재 여부 조회
def check_user_exists_by_id(db: Session, user_id: int) -> bool:
    return db.query(exists().where(User.id == user_id)).scalar()
