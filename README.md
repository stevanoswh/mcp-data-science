
# mcp-ml-e2e

End-to-end ML engineering pipeline.

## Quick-Start

```bash
# clone & run
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d        # spins all servers
# prompt LLM:
# “Ingest s3://acme/churn.csv, target=churn, full pipeline, deploy if F1 ≥ 0.80”
```
