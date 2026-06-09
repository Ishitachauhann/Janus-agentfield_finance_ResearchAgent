"""
Argus — Autonomous Investment Committee Research Agent
Exports the shared `app` Agent instance used across all modules.
"""
import os

from agentfield import Agent, AIConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Allow model to be configured dynamically, defaulting to Nebius
llm_model = os.getenv("LLM_MODEL", "nebius/openai/gpt-oss-120b")

app = Agent(
    node_id="argus-research-agent",
    ai_config=AIConfig(model=llm_model),
    # Control Plane URL is loaded dynamically from AGENTFIELD_SERVER (empty means local only)
    agentfield_server=os.getenv("AGENTFIELD_SERVER", ""),
)
