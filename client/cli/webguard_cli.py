import cmd
from agent.dns_blocker import DNSBlocker

class WebGuardShell(cmd.Cmd):
    intro = "🔒 WebGuard CLI - DNS 차단 관리\n명령어 도움말은 'help' 입력\n"
    prompt = "WebGuard> "

    def __init__(self):
        super().__init__()
        self.blocker = DNSBlocker()

    def do_list(self, arg):
        self.blocker.list_unblocked()

    def do_unblock(self, domain):
        if domain:
            self.blocker.unblock_locally(domain)
            self.blocker.apply_blacklist()
        else:
            print("❌ 도메을 입력하세요. 예: unblock example.com")
    
    def do_remove(self, domain):
        if domain:
            self.blocker.remove_local_override(domain)
            self.blocker.apply_blacklist()
        else:
            print("❌ 도메을 입력하세요. 예: remove example.com")
    
    def do_apply(self, arg):
        self.blocker.apply_blacklist()

    def do_exit(self, arg):
        print("👋 종료합니다.")
        return True
    
    def do_EOF(self, arg):
        print("👋 종료합니다.")
        return True

if __name__ == "__main__":
    WebGuardShell().cmdloop()
