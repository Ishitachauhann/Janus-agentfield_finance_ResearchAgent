"""
Equinox — Autonomous Research Agent
Exports the shared `app` Agent instance used across all modules.

Authentication is handled automatically via environment variables:
  NEBIUS_API_KEY  — used by AgentField/LiteLLM for all app.ai() calls
"""
import os
from agentfield import Agent, AIConfig
from dotenv import load_dotenv

load_dotenv()

llm_model = os.getenv("LLM_MODEL", "nebius/openai/gpt-oss-120b")

app = Agent(
    node_id="equinox-research-agent",
    # LiteLLM requires the provider prefix for Nebius Token Factory
    ai_config=AIConfig(model=llm_model),
    # Disable cloud hub connection — we run fully local, no AgentField cloud needed.
    # Without this, AgentField endlessly retries WebSocket to localhost:8080 (HTTP 403).
    agentfield_server="",
)
