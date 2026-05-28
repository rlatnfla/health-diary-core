from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db_connection import get_db_session
from app.schemas.user import UserCreate, UserHealthProfileUpdate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def _get_user_service(db: Session = Depends(get_db_session)) -> UserService:
    return UserService(db)


# 사용자 생성
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, user_service: UserService = Depends(_get_user_service)
):
    return await user_service.create_user(user_in)


# 사용자 단건 조회 API
@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_user(
    user_id: int, user_service: UserService = Depends(_get_user_service)
):
    return await user_service.read_user(user_id)


@router.put("/{user_id}/health-profile", status_code=status.HTTP_200_OK)
async def update_user_health_profile(
    user_id: int,
    profile_in: UserHealthProfileUpdate,
    user_service: UserService = Depends(_get_user_service),
):
    await user_service.modify_user_health_profile(user_id, profile_in)

    return {"message": "건강 프로필 반영 성공"}
