# T-360 Stack Review

Reviewed against `main` after PR #1 and PR #2 were merged.

## Findings

### Fixed in this branch
- Market indicator code now converts the domain model's `Decimal` prices to `float` before numerical operations. The previous implementation mixed `Decimal` and `float`, which would fail at runtime for Pydantic-created `Candle` objects.
- Added CI covering Ruff, mypy, and pytest on Python 3.12.
- Added configuration, execution-boundary, API health, and Decimal compatibility tests.
- Removed an unused market-data import.

### Design notes for later milestones
- Tick volume semantics need to be made explicit when broker adapters are implemented: cumulative exchange volume and per-tick/per-update volume require different candle aggregation rules.
- Candle/session boundaries should be driven by an exchange-calendar/session abstraction rather than assuming every UTC bucket is tradable.
- Broker interfaces should expose normalized market-data and order-event contracts, not vendor-shaped dictionaries.
- Order lifecycle needs additional states/events before live integration (for example pending, partially filled, expired, and replace/amend flows).
- AI decisions should remain a pure intent contract and be converted into `OrderRequest` only through a deterministic policy/validation layer.
- Persistence and event replay should be introduced before live order connectivity so state can be reconstructed after process restarts.

## Current verdict

The merged foundation is structurally sound, but the market-data implementation needed the Decimal compatibility fix above before it should be used as a base for broker connectivity. The next milestone should therefore merge this review/fix PR first, then proceed to the broker-neutral adapter contract and Upstox implementation.
