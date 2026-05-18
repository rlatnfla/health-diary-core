from fastapi import FastAPI
from app.api.user_router import router as user_router
from app.exceptions.handler import init_exception_handlers

app = FastAPI(
    title="Health Diary Core Server",
    description="사용자 건강 일기 데이터를 관리하고 분석 모델, NLP 서버와 통신하는 핵심 서버"
    )

# 전역 예외 처리기 마운트
init_exception_handlers(app)

# 라우터 등록
app.include_router(user_router)

@app.get("/health-check")
def read_root():
    return {
        "status" : "online"
    }