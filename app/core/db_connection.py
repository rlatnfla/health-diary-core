from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .env_loader import env

# 1. 엔진 생성
engine = create_engine(url=env.DATABASE_URL)

# 2. 세션 설정 (각 요청마다 사용할 독립적인 세션)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 모델들이 상속받을 기본 클래스
EntityBase = declarative_base()

# 4. DB 세션 획득
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()