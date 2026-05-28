from abc import ABC, abstractmethod

from app.schemas.nlp import NlpAnalysisRequestSchema


class NlpClientBase(ABC):
    """
    NLP 서버와의 통신을 정의하는 최상위 추상 클래스(interface)
    """

    @abstractmethod
    async def send_analysis_request(
        self, request_data: NlpAnalysisRequestSchema
    ) -> dict:
        """
        규격화된 데이터를 받아 외부 NLP 시스템으로 송신합니다.

        :param request_data: 통신 규격 클래스 (NlpAnalysisRequestSchema)
        :return: None (비동기 지향 구조)
        """
        pass
