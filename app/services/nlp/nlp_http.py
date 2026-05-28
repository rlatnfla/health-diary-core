import httpx

from app.exceptions.base_exception import NlpCommunicationException
from app.schemas.nlp import NlpAnalysisRequestSchema
from app.services.nlp.nlp_base import NlpClientBase


class HttpNlpClient(NlpClientBase):
    """
    HTTP 통신을 사용해 NLP 서버와 통신하는 구현체 클래스
    """

    def __init__(self, nlp_server_url: str):
        self.url = nlp_server_url

    async def send_analysis_request(
        self, request_data: NlpAnalysisRequestSchema
    ) -> dict:
        """
        pydantic DTO 구격을 받아 비동기 HTTP POST 요청을 보냅니다.
        """

        payload = request_data.model_dump()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.url}/v1/api/analyze", json=payload, timeout=10.0
                )

                response.raise_for_status()

                return response.json()

        except (httpx.HTTPError, httpx.TimeoutException):
            raise NlpCommunicationException()

    async def send_weekly_report_request(self, request_data) -> dict:
        payload = request_data.model_dump(mode="json")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.url}/v1/api/analyze/weekly", json=payload, timeout=15.0
                )
                response.raise_for_status()

                return response.json()
        except (httpx.HTTPError, httpx.TimeoutException):
            raise NlpCommunicationException()
