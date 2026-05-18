# FastAPI에 등록할 핸들러
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.base_exception import CustomBaseException

def init_exception_handlers(app: FastAPI) -> None:
    """
    FastAPI의 앱 인스턴스에 전역 예외 핸들러들을 등록하는 함수
    """

    @app.exception_handler(CustomBaseException)
    async def custom_base_exception_handler(request: Request, exc: CustomBaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code" : exc.code,
                "message" : exc.message
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        # TODO: add logger
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
            }
        )