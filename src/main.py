"""
main.py — Entry point for the Argus autonomous research agent.

Usage:
    python src/main.py
"""
import os
import sys

# Ensure the project root is on sys.path so `src` is importable
# when running as: python3 src/main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load .env before importing anything that reads env vars
load_dotenv()

# Import and boot the shared Agent instance
from src import app  # noqa: E402

# Register skills + reasoners by importing their modules.
# The @app.skill / @app.reasoner decorators fire on import.
import src.skills    # noqa: F401, E402
import src.reasoners # noqa: F401, E402
import src.stream    # noqa: F401, E402 — SSE endpoints + UI serving

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🔬 Argus Research Agent starting on http://localhost:{port}")
    print("📈 5-Agent Investment Committee:")
    print(f"   POST http://localhost:{port}/research               ← Full pipeline (all 5 agents)")
    print(f"   POST http://localhost:{port}/research/analyst       ← Bull case only")
    print(f"   POST http://localhost:{port}/research/contrarian    ← Bear case only")
    print(f"   POST http://localhost:{port}/research/stream/start  ← SSE streaming (used by UI)")
    print(f"   GET  http://localhost:{port}/                       ← Live UI")
    print()
    app.serve(port=port)
