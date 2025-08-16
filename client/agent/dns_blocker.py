import json
from pathlib import Path
from utils.config import settings
import ctypes
import os

POLICY_PATH = Path(settings.TOKEN_DIR) / "policy.json"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

class DNSBlocker:
    REDIRECT_IP = "127.0.0.1"

    def __init__(self):
        self.blocked_domains = set()
        self.load_policy()
        self.ensure_admin()

    def ensure_admin(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False
        if not is_admin:
            raise PermissionError("⚠️ 관리자 권한으로 실행해야 hosts 파일 수정 가능")

    def load_policy(self):
        if POLICY_PATH.exists():
            with open(POLICY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for site in data.get("sites", []):
                    self.blocked_domains.add(site["domain"])
            print(f"✅ {len(self.blocked_domains)}개 도메인 로드 완료")
        else:
            print("❌ 정책 파일이 없습니다. 먼저 policy_sync.py 실행 필요")

    def update_hosts_file(self):
        if not self.blocked_domains:
            return

        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines = [line for line in lines if "# WebGuard" not in line]

        for domain in self.blocked_domains:
            lines.append(f"{self.REDIRECT_IP} {domain} # WebGuard\n")

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✅ hosts 파일 업데이트 완료: {len(self.blocked_domains)}개 도메인 차단")

    def block_all(self):
        """전체 차단 수행"""
        self.update_hosts_file()


if __name__ == "__main__":
    try:
        blocker = DNSBlocker()
        blocker.block_all()
    except PermissionError as e:
        print(e)
