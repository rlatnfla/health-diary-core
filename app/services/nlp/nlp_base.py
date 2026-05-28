from abc import ABC, abstractmethod

from app.schemas.nlp import NlpAnalysisRequestSchema
from app.schemas.weekly_report import WeeklyNlpPayload


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

    @abstractmethod
    async def send_weekly_report_request(self, request_data: WeeklyNlpPayload) -> dict:
        """
        주간 누적 데이터 및 유저 건강 스냅샷을 가지고 NLP 시스템에 레포트 작성 요청
        """
        pass
