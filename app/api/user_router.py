from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.db_connection import get_db_session
from app.schemas.user import UserCreate, UserRead
from app.crud import user as user_crud 

router = APIRouter(prefix="/users", tags=["Users"])

# 1. 사용자 생성
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db_session)):
    return user_crud.create_user(db, user_in)

# 2. 사용자 목록 조회 API
@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    users = user_crud.get_users(db, skip, limit)
    return users

# 3. 사용자 단건 조회 API
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    user = user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user