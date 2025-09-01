import threading
from agent import agent
from agent.dns_blocker import DNSBlocker  # DNSBlocker 클래스 경로

stop_event = threading.Event()

def start_agent():
    agent.run()  # 기존 Agent 서버 실행

def start_dns():
    blocker = DNSBlocker()       # DNSBlocker 인스턴스 생성
    blocker.apply_blacklist()    # hosts 업데이트 + DNS 캐시 플러시
    # 기존 dns_blocker.run() 제거, 필요 시 run() 안에 포함시키면 됨

if __name__ == "__main__":
    t1 = threading.Thread(target=start_agent, daemon=True)
    t2 = threading.Thread(target=start_dns, daemon=True)

    t1.start()
    t2.start()

    # 불필요한 print 제거, 프로그램 종료 방지
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        stop_event.set()
