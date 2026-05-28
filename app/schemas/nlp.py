from datetime import date

from pydantic import BaseModel


class NlpAnalysisRequestSchema(BaseModel):
    """
    core 서버가 NLP 서버로 보낼 공통 데이터 규격 DTO
    """

    content: str


# api DTO
class DiaryCreate(BaseModel):
    user_id: int
    date: date
    content: str
