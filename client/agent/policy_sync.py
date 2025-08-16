import json
from pathlib import Path
import requests
from utils.config import settings

POLICY_PATH = Path(settings.TOKEN_DIR) / "policy.json"

def save_policy(data: dict):
    POLICY_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

def download_policy():
    url = f"{settings.SERVER_URL}/policy/blacklist"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        save_policy(data)
        print(f"✅ 정책 다운로드 완료 (총 {len(data.get('sites', []))}개 항목)")
    except requests.RequestException as e:
        print(f"❌ 정책 다운로드 실패: {e}")

if __name__ == "__main__":
    download_policy()
