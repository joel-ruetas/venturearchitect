from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .agents.root_agent import venture_architect_root_agent

# FastAPI/Starlette application exposing VentureArchitect via A2A protocol.
app = to_a2a(venture_architect_root_agent, port=8001)
