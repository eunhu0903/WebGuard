import threading
from agent import agent
from agent import dns_blocker

stop_event = threading.Event()

def start_agent():
    agent.run()

def start_dns():
    dns_blocker.run()

if __name__ == "__main__":
    t1 = threading.Thread(target=start_agent)
    t2 = threading.Thread(target=start_dns)

    t1.start()
    t2.start()

    print("✅ Agent + DNS + Block Server 실행 중 (Ctrl+C로 종료)")
