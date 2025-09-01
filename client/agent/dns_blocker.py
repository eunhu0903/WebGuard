import json
import os
import ctypes
import sys
import subprocess
from pathlib import Path
from utils.config import settings

HOSTS_PATH = Path(os.path.expandvars(settings.HOSTS_PATH))
POLICY_PATH = Path(settings.POLICY_PATH)
LOCAL_OVERRIDE_PATH = Path(os.path.expandvars(settings.LOCAL_OVERRIDE_PATH))
REDIRECT_IP = "127.0.0.1"

class DNSBlocker:
    def __init__(self):
        self.blocked_domains = set()
        self.local_override = set()
        self.load_policy()
        self.load_local_override()
        self.ensure_admin()

    def ensure_admin(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False
        if not is_admin:
            print("⚠️ 관리자 권한 필요합니다. 프로그램을 종료합니다.")
            sys.exit(1)
    
    def flush_dns_windows(self):
        try:
            subprocess.run(["ipconfig", "/flushdns"], check=True)
            print("🔄 Windows DNS 캐시 플러시 완료")
        except subprocess.CalledProcessError:
            print("❌ DNS 캐시 플러시 실패. 관리자 권한 확인 필요")

    def load_policy(self):
        if POLICY_PATH.exists():
            with open(POLICY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.blocked_domains = set(site["domain"] for site in data.get("sites", []))
        else:
            print("❌ 정책 파일 없음")
    
    def get_unblocked_domains(self):
        return list(self.local_override)

    def get_blocked_domains(self):
        return [d for d in self.blocked_domains if d not in self.local_override]

    def load_local_override(self):
        if LOCAL_OVERRIDE_PATH.exists():
            with open(LOCAL_OVERRIDE_PATH, "r", encoding="utf-8") as f:
                self.local_override = set(json.load(f))
        else:
            self.local_override = set()

    def save_local_override(self):
        LOCAL_OVERRIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOCAL_OVERRIDE_PATH, "w", encoding="utf-8") as f:
            json.dump(list(self.local_override), f, indent=2)

    def apply_blacklist(self):
        if not self.blocked_domains:
            return

        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines = [line for line in lines if "# WebGuard" not in line]

        for domain in self.blocked_domains:
            if domain not in self.local_override:
                lines.append(f"{REDIRECT_IP} {domain} # WebGuard\n")

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✅ hosts 파일 업데이트 완료 ({len(self.blocked_domains)}개 도메인 적용)")

        self.flush_dns_windows()
        print("✅ DNS 캐시 플러시 완료, 브라우저를 재시작하면 차단이 바로 적용됩니다.")

    def unblock_locally(self, domain: str):
        if domain in self.blocked_domains:
            self.local_override.add(domain)
            self.save_local_override()
            print(f"{domain} 로컬 차단 해제 완료")
        else:
            print(f"{domain}는 블랙리스트에 없습니다")

    def list_unblocked(self):
        if not self.local_override:
            print("로컬 차단 해제된 도메인 없음")
            return
        print("로컬 차단 해제 도메인 목록:")
        for d in self.local_override:
            print("-", d)

    def remove_local_override(self, domain: str):
        if domain in self.local_override:
            self.local_override.remove(domain)
            self.save_local_override()
            print(f"{domain} 로컬 차단 해제 목록에서 삭제")
        else:
            print(f"{domain}는 로컬 차단 해제 목록에 없음")

def run():
    print("✅ DNS 차단 적용 완료")