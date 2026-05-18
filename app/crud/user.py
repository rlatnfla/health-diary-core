from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

# 사용자 생성
def create_user(db: Session, user_in: UserCreate):
    db_user = User(
        name = user_in.name,
        gender = user_in.gender,
        birth_date = user_in.birth_date
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 단건 조회
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 사용자 목록 조회
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()
