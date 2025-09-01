import os
import platform
import requests
from utils.token import save_token, load_token
from utils.config import settings

class Agent:
    def __init__(self):
        self.server_url = settings.SERVER_URL
        self.token_dir = settings.TOKEN_DIR
        os.makedirs(self.token_dir, exist_ok=True)
        self.token_path = os.path.join(self.token_dir, "agent_token.json")
        self.agent_id = None

    def run(self):
        """Agent 실행: 기존 토큰 확인 후 없으면 서버 등록"""
        token_data = load_token()
        if token_data and "agent_id" in token_data:
            self.agent_id = token_data["agent_id"]
            print(f"✅ 이미 등록된 에이전트: {self.agent_id}")
        else:
            print("🔑 에이전트 없음, 서버 등록 중...")
            self.register_and_save()

    def register_and_save(self):
        """서버에서 Agent ID 발급 및 저장"""
        try:
            data = self.register_agent()
            self.agent_id = data["agent_id"]
            save_token({"agent_id": self.agent_id})
            print(f"✅ 서버 등록 완료: {self.agent_id}")
        except Exception as e:
            print(f"❌ 서버 등록 실패: {e}")

    def register_agent(self):
        """서버 API 호출, JSON 결과 반환"""
        url = f"{self.server_url}/agent/install"
        payload = {
            "os": platform.system(),
            "version": "1.0.0"
        }
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()


def run():
    Agent().run()
