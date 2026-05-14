from fastapi import FastAPI

app = FastAPI(
    title="Health Diary Core Server",
    description="사용자 건강 일기 데이터를 관리하고 분석 모델, NLP 서버와 통신하는 핵심 서버"
    )

@app.get("/health-check")
def read_root():
    return {
        "status" : "online"
    }