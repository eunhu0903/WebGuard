import requests
from .config import settings

def register_agent(agent_id: str) -> str:
    url = f"{settings.SERVER_URL}/agent/register"
    resp = requests.post(url, json={"agent_id": agent_id})
    resp.raise_for_status()
    return resp.json().get("access_token") 