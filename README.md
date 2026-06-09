# Building a Production-Ready Multi-Agent Investment Committee with AgentField (Equinox 🔬)

An autonomous financial research agent built on [AgentField](https://dub.sh/agentf). This project uses a **5-agent Investment Committee** to produce two parallel research reports — one for **short-term** (1-6 months) and one for **long-term** (1-5 year) investment horizons.

To support the project under standard Google Gemini Free Tier quotas (which have a strict 5 Requests Per Minute rate limit and a 20 Requests Per Day limit on the standard Flash model), the project executes the committee **sequentially** with **12-second throttling pauses** between LLM requests. It is configured to run on `gemini-2.5-flash-lite` (which supports high-volume daily requests on the free tier).

(for Concurrency & Speed: The Analyst and Contrarian run in parallel. Then both Editors run in parallel. This is true concurrency via asyncio.gather, not sequential execution. teh goal was to -Dispatche LLM requests in parallel (asyncio.gather). Works only on paid/high-quota keys.)---- 
instead have used Sequential Throttling (12s pauses). We serialized the agent runs to prevent hitting the 5 RPM rate limit on your free Gemini key.


---

## Architecture

```
User Query
    │
[1] Manager       ── Decomposes query ──> ResearchPlan
    │
[2] yfinance      ── 9 data fetches in parallel (asyncio.gather)
    │                annual + quarterly income/cashflow, balance sheet,
    │                company facts, analyst price targets, insider
    │                transactions, news (20 articles)
    │
[3] Analyst   ───┐ ── LLM calls run sequentially with 12s delay (to respect rate limits)
[3] Contrarian ──┘    Both see: financials, targets, insiders, news
    │
[4] EditorShort ─┐ ── Sequential LLM calls with 12s delay (to respect rate limits)
[4] EditorLong  ─┘    Short: quarterly trends + near-term signals
                      Long:  annual data + moat + valuation
    │
DualResearchReport ──> Tabbed UI (Short Term | Long Term)
```

### The Investment Committee

| Agent | Default Model | Role | Runs |
| --- | --- | --- | --- |
| **Manager** | gemini-2.5-flash-lite | Decomposes query, dispatches committee | Sequential |
| **Analyst** | gemini-2.5-flash-lite | Bull case: revenue, margins, growth, free cash flow, catalysts | **Sequential (12s Sleep)** |
| **Contrarian** | gemini-2.5-flash-lite | Bear case: risks, lawsuits, competition, valuation | **Sequential (12s Sleep)** |
| **EditorShort** | gemini-2.5-flash-lite | Short-term verdict (1-6 months) — focuses on catalysts & momentum | **Sequential (12s Sleep)** |
| **EditorLong** | gemini-2.5-flash-lite | Long-term verdict (1-5 years) — focuses on moat & intrinsic value | **Sequential (12s Sleep)** |
| **Skills** | - | yfinance wrappers: 7 data endpoints, all fetched in parallel | Parallel |

---

## Setup & Configuration

### 1. Prerequisites
- Python 3.8 - 3.12
- A Google Gemini API key

### 2. Install Dependencies
Initialize your virtual environment and install the required packages:
```bash
# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```env
LLM_MODEL=gemini/gemini-2.5-flash-lite
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8080
```

*Note: The project loads `LLM_MODEL` dynamically. By utilizing `gemini/gemini-2.5-flash-lite`, you avoid the strict 20-request daily limit of the experimental flash preview, allowing extensive research sessions.*

### 4. Run the Server
Launch the FastAPI server:
```bash
python src/main.py
```
The agent server will start on `http://localhost:8080`.

### 5. Open the UI
Open **http://localhost:8080** in your browser. Type any query (e.g. *"Should I invest in NVDA?"*) and watch the 5-agent committee work in real-time. Status badges update to show the throttling states, thought logs print live, and a complete report renders when the editors finish.

---

## Usage / API Options

Equinox exposes two ways to run the full 5-agent pipeline:

### Option A — Streaming API (used by the UI)
Sends events in real-time as each agent completes.
- **Start Session**: `POST /research/stream/start` with body `{"query": "<your question>"}` -> returns `session_id`.
- **Read SSE Stream**: `GET /research/stream/events/{session_id}` -> yields real-time JSON events (`agent_start`, `agent_note`, `agent_complete`, `complete`).

### Option B — Standalone API
Returns the final synthesized report directly in a single block.
- **Query Endpoint**: `POST /research` with body `{"query": "<your question>"}` -> returns the full `DualResearchReport` JSON.
