import logging
from functools import wraps

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def transactional(read_only: bool = False):
    """
    메서드용 AOP transaction 데코레이터

    Args:
        read_only (bool, optional): 읽기 전용 모드 여부. True일 경우 commit을 수행하지 않습니다.

    Returns:
        function: 실제 메서드를 가로채는 decorator 함수를 반환합니다.
    """

    def decorator(func):
        """
        Args:
            func (function) 사용자가 작성한 원본 서비스 메서드

        Returns:
            function: 트랜잭션 로직이 주입된 wrapper 함수를 반환합니다.
        """

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            """
            Args:
                self: 서비스 클래스의 인스턴스
                *args: 원본 메서드가 받던 일반 파라미터들
                **kwargs: 원본 메서드가 받던 키워드 파라미터들

            Returns:
                any: 원본 비즈니스 메서드가 리턴하는 최종 결과값
            """

            db: Session | None = None

            for attr_name in dir(self):
                attr_value = getattr(self, attr_name)
                if isinstance(attr_value, Session):
                    db = attr_value
                    break

            if db is None:
                raise AttributeError(
                    "[@transactional] 에러: 해당 서비스 클래스 내부에 주입된 SQLAlchemy Session 객체를 찾을 수 없습니다."
                )

            original_autoflush = db.autoflush

            try:
                if read_only:
                    # 변경 감지(autoflush)를 해제하여 메모리 및 CPU 연산 최적화
                    db.autoflush = False

                    # 명시적 읽기 전용 트랜잭션 옵션 부여
                    db.begin(nested=db.in_transaction())
                    db.execute(text("SET TRANSACTION READ ONLY"))

                else:
                    if not db.in_transaction():
                        db.begin()

                result = await func(self, *args, **kwargs)

                if not read_only:
                    db.commit()
                else:
                    # 읽기 전용 모드일 시 무조건 rollback으로 안전하게 닫음
                    db.rollback()

                return result

            except Exception as e:
                db.rollback()
                logger.error(
                    f"[@transactional] 에러 발생으로 인한 트랜잭션 롤백: {str(e)}"
                )
                raise e

            finally:
                db.autoflush = original_autoflush

        return wrapper

    return decorator
