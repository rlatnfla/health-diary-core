# 커스텀 예외 및 에러 DTO 정의
from pydantic import BaseModel

class ErrorResponseSchema(BaseModel):
    code: str
    message: str

class CustomBaseException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code  # HTTP 상태 코드 (예: 404, 500)
        self.code = code                # 내부 에러 코드 (예: "ERR_001")
        self.message = message
        super().__init__(message)

class ResourceNotFoundException(CustomBaseException):
    def __init__(self, resource_name: str):
        super().__init__(status_code=404, code="ERR_RESOURCE_NOT_FOUND", message=f"{resource_name}를 찾을 수 없습니다.")

class NlpCommunicationException(CustomBaseException):
    def __init__(self):
        super().__init__(status_code=502, code="ERR_NLP_SERVER_COMMUNICATION", message="NLP 서버와의 통신 중 오류가 발생했습니다.")