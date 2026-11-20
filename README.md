# GAHENAX Trader — Binance Spot Testnet

Read-only cloud diagnostic for Binance Spot Testnet. **No order execution is enabled.**

## Setup on Render
1. Deploy using `render.yaml` (free web service).
2. In Render > Service > Environment set `TESTNET_API_KEY` and `TESTNET_API_SECRET` as secret environment variables. Never commit keys.
3. The service exposes `/health` only; it does not expose balances, API keys or account data.
4. To verify the signed account, use the Render Shell (if available) to run `python scripts/testnet_probe.py --account`. Otherwise a separate one-off job can be added later.

**Important:** Make this repository private before storing any proprietary strategy code. Do not configure live Binance credentials.
