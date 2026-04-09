import os
from dotenv import load_dotenv

load_dotenv(override=True)

brave_api_key = os.getenv("BRAVE_API_KEY", "")
brave_env = {"BRAVE_API_KEY": brave_api_key}
MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY", "")
polygon_plan = os.getenv("MASSIVE_PLAN", "free")

is_paid_polygon = polygon_plan == "paid"
is_realtime_polygon = polygon_plan == "realtime"
has_real_brave_key = brave_api_key and brave_api_key != "test_key_for_now"

if is_paid_polygon or is_realtime_polygon:
    market_mcp = {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"],
        "env": {"MASSIVE_API_KEY": MASSIVE_API_KEY},
    }
else:
    market_mcp = {"command": "uv", "args": ["run", "src/mcp_servers/market_server.py"]}

trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "src/mcp_servers/accounts_server.py"]},
    {"command": "uv", "args": ["run", "src/mcp_servers/push_server.py"]},
    {"command": "uv", "args": ["run", "src/mcp_servers/news_server.py"]},
    market_mcp,
]

def researcher_mcp_server_params(name: str):
    servers = []
    return servers

risk_manager_mcp_server_params = [
    {"command": "uv", "args": ["run", "src/mcp_servers/accounts_server.py"]},
    market_mcp,
]
