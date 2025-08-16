import json
from pathlib import Path
import ctypes
from utils.config import settings
from utils.token import load_token
from .logger import BlockLogger

POLICY_PATH = Path(settings.TOKEN_DIR) / "policy.json"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

class DNSBlocker:
    REDIRECT_IP = "127.0.0.1"

    def __init__(self):
        self.blocked_domains = set()
        self.load_policy()
        self.ensure_admin()

        token_data = load_token()
        self.agent_id = token_data.get("agent_id") if token_data else None
        self.logger = BlockLogger(self.agent_id) if self.agent_id else None

    def ensure_admin(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False
        if not is_admin:
            print("⚠️ 관리자 권한으로 실행해야 hosts 파일 수정 가능")

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

        # 이전 WebGuard 항목 제거
        lines = [line for line in lines if "# WebGuard" not in line]

        for domain in self.blocked_domains:
            lines.append(f"{self.REDIRECT_IP} {domain} # WebGuard\n")
            # 차단 로그 기록
            if self.logger:
                self.logger.add_log(domain)

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✅ hosts 파일 업데이트 완료: {len(self.blocked_domains)}개 도메인 차단")

    def block_all(self):
        self.update_hosts_file()
        # 차단 로그 서버 업로드
        if self.logger:
            self.logger.upload_logs()

    def unblock_all(self):
        if not POLICY_PATH.exists():
            return
        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # WebGuard 항목 제거
        lines = [line for line in lines if "# WebGuard" not in line]
        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("✅ 모든 차단 해제 완료")


if __name__ == "__main__":
    blocker = DNSBlocker()
    blocker.block_all()
    blocker.unblock_all()
    print("✅ 차단 해제 완료")
