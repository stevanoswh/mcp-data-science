# CLAUDE.md

# Project: mcp-ml-e2e

> **Purpose**  Enable Claude Code to run, observe, and extend a full ML‑engineering pipeline—ingest → validate → train → evaluate → deploy → monitor—exposed through **Model Context Protocol (MCP)** servers. This file is Claude’s single source of truth, so keep it concise, practical, and always up‑to‑date.

---

## 📑 Table of Contents

1. What this repo does
2. Directory layout
3. Quick‑start (local & cloud)
4. MCP servers & config
5. Prompt patterns: talking to Claude
6. Allowed tools & scopes
7. Dev conventions & best practices
8. Troubleshooting
9. Extending the pipeline
10. Changelog

> Jump straight to §5 if you just want prompt examples.

---

\## 1 · 🚀 What this repo does
End‑to‑end ML‑engineering pipeline that a Large‑Language‑Model agent can control **without extra glue‑code**. Each stage is a lightweight MCP server:

```text
DataOps  ➜ Feature ➜ Trainer ➜ Deployer (+ Monitor)
```

Claude Code (the host) sees them through a single `.mcp.json` manifest and calls their tools via structured JSON.

**Key results**

* ⏱ «Push‑button» latency: raw data → production in ≤ 15 min for 1 M rows.
* 🛡 Safe‑by‑default: mTLS, JWT scopes, resource quotas.
* 🔍 Fully observable: OTEL traces, Prometheus metrics, JSON logs.

---

\## 2 · 🗄️ Directory layout

```text
servers/           # one MCP server per stage
  dataops.py       # ingest_s3, validate_df
  feature.py       # encode_cat, impute_null
  trainer.py       # train, evaluate
  deployer.py      # push_k8s, monitor_drift, rollback
.mcp.json          # autostart & URL map for all servers
workflows/pipe.py  # LangGraph DAG example
.docker/           # container specs for each server
.claude/commands/  # slash commands (see §5)
README.md          # human‑friendly intro
CLAUDE.md          # ← this file (Claude loads on start‑up)
```

---

\## 3 · ⚡ Quick‑start
\### Local dev (Docker Compose)

```bash
# 1 · clone & install deps
git clone https://github.com/your‑org/mcp‑ml‑e2e && cd mcp‑ml‑e2e
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2 · spin everything up
docker compose up ‑d            # starts all MCP servers

# 3 · open Claude Code and start prompting (see §5)
```

\### Cloud (Kubernetes)

```bash
helm repo add mcp https://charts.your‑org.dev && \
helm upgrade --install mcp‑ml‑e2e mcp/stack -f charts/values.yaml
```

> **Tip:** set `global.jwtIssuer` & `global.caBundle` in `values.yaml` before deploying.

---

\## 4 · 🛠 MCP servers & config
`.mcp.json` tells Claude how to start—or reach—every server:

```jsonc
// .mcp.json – checked‑in so the whole team can «just work»
{
  "dataops":  { "command": "python", "args": ["servers/dataops.py"] },
  "feature":  { "command": "python", "args": ["servers/feature.py"] },
  "trainer":  { "command": "python", "args": ["servers/trainer.py"] },
  "deployer": { "command": "python", "args": ["servers/deployer.py"] }
}
```

If you run servers remotely, replace the object with `"url": "https://..."`.

Each server registers its tools and JSON Schema automatically via **FastMCP 2.x**.

---

\## 5 · 🗨️ Prompt patterns: talking to Claude
Claude understands three «speech acts».

| Pattern               | Example                                                                                           | What happens                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Declarative order** | *“Ingest s3://acme/churn.csv as churn dataset, train random‑forest (n=300), deploy if F1 ≥ 0.80”* | Claude plans a DAG and calls tools with sensible defaults.           |
| **Slash command**     | `/train n_estimators=500 criterion=gini`                                                          | Direct call to `trainer/train`. Aliases live in `.claude/commands/`. |
| **Inspection / why**  | “Show the metrics of the last run”                                                                | Claude queries `trainer/evaluate` and streams the JSON.              |

> 🧠 **Best practice:** keep prompts imperative, one sentence per stage, thresholds explicit.

---

\## 6 · 🔐 Allowed tools & JWT scopes
Add these scopes to your Claude workspace or `/permissions`:

```
mcp__dataops__ingest_s3
mcp__dataops__validate_df
mcp__feature__encode_cat
mcp__feature__impute_null
mcp__trainer__train
mcp__trainer__evaluate
mcp__deployer__push_k8s
mcp__deployer__monitor_drift
mcp__deployer__rollback
```

**Security defaults**

* Transport = HTTP/2 over TLS 1.3 (mTLS enforced).
* JWT `aud` = `mcp‑ml‑e2e`; scopes checked per tool.
* Resource limits: CPU ≤ 4, RAM ≤ 8 GiB unless overridden in manifest.

---

\## 7 · 🛠️ Dev conventions & best practices

* **Schema‑first** – Every tool declares strict JSON Schema; Claude auto‑validates.
* **Atomic** – One function = one side‑effect‑free action. Return paths or IDs, never raw binaries.
* **Versioning** – `FastMCP(name, version="X.Y.Z")`, artifact = `model‑${git‑sha}.joblib`.
* **Observability** – `mcp.use_logging()` + OTEL exporter; Prometheus at `/metrics`.
* **Testing** – PyTest for unit + contract tests; Vitest for TS parts. CI blocks merge on failures.

---

\## 8 · 🩹 Troubleshooting

| Symptom                          | Fix                                                                  |
| -------------------------------- | -------------------------------------------------------------------- |
| *Claude says “tool not allowed”* | Check §6 scopes.                                                     |
| *Timeout during train*           | Increase `timeout` field in `.mcp.json` or lower dataset size.       |
| *Deployment URL 404*             | Run `deployer/monitor_drift` to confirm pod status, then `rollback`. |

---

\## 9 · ➕ Extending the pipeline

1. Create a new server file in `servers/` (e.g., `tuner.py`).
2. Define tools with `@mcp.tool(schema=…)`.
3. Add entry to `.mcp.json`.
4. Update allowed scopes (§6) and prompts (§5).

> Claude picks up new tools automatically after restart.

---

\## 10 · 📜 Changelog

| Version  | Date         | Notes                                                         |
| -------- | ------------ | ------------------------------------------------------------- |
|  v0.3.0  |  2025‑06‑28  | First public release; added Feature server and rollback tool. |
|  v0.2.0  |  2025‑06‑12  | Integrated OTEL + Prometheus.                                 |
|  v0.1.0  |  2025‑05‑30  | MVP: ingest → train → deploy.                                 |

---

**Maintainers**  \<github‑handle1>, \<github‑handle2>  • Reach us in `#mcp‑ml‑e2e` Slack channel.
