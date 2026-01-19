import os
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 로드
load_dotenv()

class Config:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.config_path = self.root_dir / "config.json"
        
        # 기본값 설정
        self.port = int(os.getenv("PORT", 8123))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # JSON 설정 로드
        self.nws_api_base = "https://api.weather.gov"
        self.user_agent = "weather-mcp-server/1.0"
        self.timeout = 30.0
        
        self._load_json_config()

    def _load_json_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.nws_api_base = data.get("nws_api_base", self.nws_api_base)
                self.user_agent = data.get("user_agent", self.user_agent)
                if "timeouts" in data:
                    self.timeout = data["timeouts"].get("read", 30.0)

# 전역 설정 인스턴스
settings = Config()