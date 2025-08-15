import os
from utils.token import save_token, load_token
from utils.config import settings
import requests
import platform

class Agent:
    def __init__(self):
        self.server_url = settings.SERVER_URL
        self.token_dir = settings.TOKEN_DIR
        os.makedirs(self.token_dir, exist_ok=True)
        self.token_path = os.path.join(self.token_dir, "agent_token.json")
        self.agent_id = None

    def run(self):
        token_data = load_token()
        if token_data:
            self.agent_id = token_data.get("agent_id")
            print(f"✅ 이미 등록된 에이전트: {self.agent_id}")
        else:
            print("🔑 에이전트 없음, 서버 등록 중...")
            self.register_and_save()

    def register_and_save(self):
        """서버에서 Agent ID 발급"""
        try:
            response = self.register_agent()
            response.raise_for_status()
            data = response.json()
            self.agent_id = data["agent_id"]
            save_token({"agent_id": self.agent_id})
            print(f"✅ 서버 등록 완료: {self.agent_id}")
        except requests.RequestException as e:
            print(f"❌ 서버 등록 실패: {e}")

    def register_agent(self):
        """서버 API 호출"""
        url = f"{self.server_url}/agent/install"
        payload = {
            "os": platform.system(),
            "version": "1.0.0"
        }
        return requests.post(url, json=payload)

if __name__ == "__main__":
    agent = Agent()
    agent.run()
