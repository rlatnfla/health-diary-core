from sqlalchemy.orm import Session

from app.core.decorators import transactional
from app.dao import user as user_dao
from app.exceptions.base_exception import ResourceNotFoundException
from app.models.user import User
from app.schemas.user import UserCreate, UserHealthProfileUpdate, UserRead


class UserService:
    """
    유저 도메인 비즈니스 로직 총괄 서비스 레이어
    """

    def __init__(self, db: Session):
        self.db = db

    @transactional()
    async def create_user(self, user_in: UserCreate) -> UserRead:

        # TODO: unique 칼럼 추가 되면 중복 로직 추가

        new_user = user_dao.create_user(self.db, user_in)

        return UserRead.model_validate(new_user)

    @transactional(read_only=True)
    async def read_user(self, user_id: int) -> UserRead:
        db_user = user_dao.get_user_by_id(self.db, user_id)
        if db_user is None:
            raise ResourceNotFoundException("사용자")

        return UserRead.model_validate(db_user)

    @transactional(read_only=True)
    async def validate_user_exists(self, user_id: int) -> None:
        exists = user_dao.check_user_exists_by_id(self.db, user_id)

        if not exists:
            raise ResourceNotFoundException("사용자")

    @transactional()
    async def modify_user_health_profile(
        self, user_id: int, profile_in: UserHealthProfileUpdate
    ) -> None:
        db_user = user_dao.get_user_by_id(self.db, user_id)
        if not db_user:
            raise ResourceNotFoundException("사용자")

        db_user.update_health_profile(profile_in)

    @transactional(read_only=True)
    async def read_user_with_health_data(self, user_id: int) -> User:
        db_user = user_dao.get_user_by_id(self.db, user_id)
        if db_user is None:
            raise ResourceNotFoundException("사용자")

        return db_user
