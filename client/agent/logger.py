import json
import requests
from pathlib import Path
from utils.config import settings
from datetime import datetime, timezone

LOG_PATH = Path(settings.TOKEN_DIR) / "block_logs.json"

class BlockLogger:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.server_url = settings.SERVER_URL
        self.logs = []

        # 로컬에 저장된 로그 불러오기
        self.load_logs()

    def add_log(self, domain: str, action: str = "blocked"):
        """차단 이벤트 추가"""
        entry = {
            "site_domain": domain,
            "action": action,
            "attempted_at": datetime.utcnow().isoformat()  # ISO 8601 문자열
        }
        self.logs.append(entry)
        self.save_logs()

    def save_logs(self):
        """로컬 JSON 저장"""
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump({"agent_id": self.agent_id, "logs": self.logs}, f, ensure_ascii=False, indent=2)

    def load_logs(self):
        """로컬 JSON 불러오기"""
        if LOG_PATH.exists():
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.logs = data.get("logs", [])

    def upload_logs(self):
        """서버로 업로드"""
        if not self.logs:
            print("ℹ️ 업로드할 로그가 없습니다.")
            return

        payload = {"logs": []}
        for log in self.logs:
            payload["logs"].append({
                "site_domain": log["site_domain"],
                "action": log["action"],
                "attempted_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            })

        try:
            resp = requests.post(f"{self.server_url}/logs/upload", json=payload, timeout=5)
            resp.raise_for_status()
            print(f"✅ {len(self.logs)}개 로그 서버 업로드 완료")
            self.logs = []  # 업로드 후 초기화
            self.save_logs()
        except requests.RequestException as e:
            print(f"❌ 로그 업로드 실패: {e}")
