import argparse
from agent.dns_blocker import DNSBlocker

def main():
    parser = argparse.ArgumentParser(description="WebGuard CLI - 로컬 차단 해제 전용")
    parser.add_argument("--unblock", help="도메인 로컬 차단 해제")
    parser.add_argument("--list", action="store_true", help="로컬 차단 해제 목록 확인")
    parser.add_argument("--remove", help="로컬 차단 해제 목록에서 제거")

    args = parser.parse_args()
    blocker = DNSBlocker()

    if args.unblock:
        blocker.unblock_locally(args.unblock)
        blocker.apply_blacklist()  # hosts 파일에 반영
    elif args.list:
        blocker.list_unblocked()
    elif args.remove:
        blocker.remove_local_override(args.remove)
        blocker.apply_blacklist()  # hosts 파일에 반영
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
