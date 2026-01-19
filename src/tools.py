from typing import Dict, Any
from .server import mcp
from .api_client import nws_client

def _format_alert(feature: Dict[str, Any]) -> str:
    """Alert 데이터를 읽기 쉬운 문자열로 변환 (헬퍼 함수)"""
    props = feature.get("properties", {})
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    data = await nws_client.get_alerts_by_state(state)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [_format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # 1. 포인트 데이터 조회
    points_data = await nws_client.get_points(latitude, longitude)
    if not points_data:
        return "Unable to fetch forecast data for this location."

    # 2. 예보 URL 추출
    properties = points_data.get("properties", {})
    forecast_url = properties.get("forecast")
    
    if not forecast_url:
        return "Forecast URL not found in point data."

    # 3. 상세 예보 조회
    forecast_data = await nws_client.get_forecast_from_url(forecast_url)
    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # 4. 결과 포맷팅
    periods = forecast_data.get("properties", {}).get("periods", [])
    forecasts = []
    
    for period in periods[:5]:  # 다음 5개 구간만 표시
        forecast = f"""
{period.get('name')}:
Temperature: {period.get('temperature')}°{period.get('temperatureUnit')}
Wind: {period.get('windSpeed')} {period.get('windDirection')}
Forecast: {period.get('detailedForecast')}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)