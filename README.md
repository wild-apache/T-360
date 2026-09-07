# T-360

T-360 is a modular trading platform for Indian markets, designed around broker-neutral market data, deterministic execution, pluggable strategies, and an AI decision layer.

## Current status

The repository currently contains the foundation scaffold. Broker integrations and live market connectivity are intentionally isolated behind interfaces so the rest of the system does not depend on one vendor.

### Planned runtime flow

```text
Broker WebSocket
      ↓
Market Data Engine → Indicators / Features
      ↓
Strategy / Scanner
      ↓
AI Decision Layer
      ↓
Structured Trading Intent
      ↓
Execution Engine
      ↓
Broker Adapter
      ↓
Order / Fill Stream
```

## Modes

- `backtest` — historical/replay execution
- `paper` — simulated execution against live market data
- `live` — broker execution

Set `T360_TRADING_MODE` in the environment. Credentials must remain outside source control.

## Development

Python 3.12+ is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn t360.api.main:app --reload
```

Health endpoint: `GET /health`.

## Architecture principles

1. Broker adapters implement a common interface.
2. The AI layer emits validated structured decisions; it does not call broker APIs directly.
3. Market data and order state are event-driven.
4. Strategies are replaceable modules.
5. Backtest, paper, and live modes share the same domain contracts where practical.
6. Secrets are supplied through environment/deployment configuration, never committed to Git.
