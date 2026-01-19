import uvicorn
import argparse
from src.config import settings
from src.server import mcp
import src.tools  # 중요: 도구 등록을 위해 모듈을 임포트해야 함

def main():
    parser = argparse.ArgumentParser(description="MCP Weather Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.port, 
        help=f"Port to listen on (default: {settings.port})"
    )
    args = parser.parse_args()

    print(f"Starting MCP Weather Server on port {args.port}...")
    print(f"NWS API Base: {settings.nws_api_base}")

    # Streamable HTTP 전송 방식으로 서버 시작
    uvicorn.run(
        mcp.streamable_http_app, 
        host="0.0.0.0", 
        port=args.port
    )

if __name__ == "__main__":
    main()