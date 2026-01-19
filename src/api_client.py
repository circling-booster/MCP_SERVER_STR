import httpx
from typing import Any, Optional, Dict
from .config import settings

class NWSClient:
    """National Weather Service API와의 통신을 담당하는 클라이언트"""
    
    def __init__(self):
        self.base_url = settings.nws_api_base
        self.headers = {
            "User-Agent": settings.user_agent,
            "Accept": "application/geo+json"
        }

    async def _request(self, url: str) -> Optional[Dict[str, Any]]:
        """내부 요청 헬퍼 함수"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, 
                    headers=self.headers, 
                    timeout=settings.timeout
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}") # 실제 운영시 로거 사용 권장
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    async def get_alerts_by_state(self, state: str) -> Optional[Dict[str, Any]]:
        """주(State)별 경보 조회"""
        url = f"{self.base_url}/alerts/active/area/{state}"
        return await self._request(url)

    async def get_points(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """좌표에 대한 포인트 메타데이터 조회"""
        url = f"{self.base_url}/points/{latitude},{longitude}"
        return await self._request(url)

    async def get_forecast_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """특정 URL(forecast URL)에서 예보 조회"""
        return await self._request(url)

# 싱글톤처럼 사용할 수 있도록 인스턴스 생성
nws_client = NWSClient()