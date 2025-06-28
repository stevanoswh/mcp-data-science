# Developer Guide: mcp-ml-e2e

This guide provides instructions on how to set up, run, and interact with the end-to-end machine learning pipeline.

---

## 1. Project Overview

This project provides a single-command, end-to-end ML engineering pipeline that an LLM agent can run through Model Context Protocol (MCP) calls. The goal is to automate the process from raw data ingestion to model deployment and monitoring.

The pipeline consists of four main services, each running as a separate MCP server:
- **DataOps:** Handles data ingestion and validation.
- **Feature:** Performs feature engineering tasks like encoding and imputation.
- **Trainer:** Trains and evaluates the machine learning model.
- **Deployer:** Deploys the trained model to a Kubernetes-like environment and monitors for drift.

---

## 2. Setup and Installation

Follow these steps to get the project running locally.

### Prerequisites
- Python 3.8+ and `pip`
- Docker and `docker-compose`

### Installation
1.  **Clone the repository** (if you haven't already).

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    *On Windows, use `.venv\Scripts\activate`.*

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Running the Services

All services are containerized and managed by Docker Compose.

1.  **Build and start all services in the background:**
    ```bash
    docker compose up -d --build
    ```
    This command builds the Docker image for the services and starts a container for each one (`dataops`, `feature`, `trainer`, `deployer`).

2.  **Verify the services are running:**
    ```bash
    docker compose ps
    ```
    You should see all four services listed with a "running" status. The services will be available at the following local ports:
    - `dataops`: `http://localhost:8001`
    - `feature`: `http://localhost:8002`
    - `trainer`: `http://localhost:8003`
    - `deployer`: `http://localhost:8004`

3.  **To stop the services:**
    ```bash
    docker compose down
    ```

---

## 4. Interacting with the Pipeline

The pipeline is designed to be driven by an LLM agent (like Gemini) that can make `call_tool` requests to the different MCP servers. The `workflows/pipe.py` script provides a reference implementation for the orchestration logic.

### Example Workflow

An LLM agent would perform the following steps to run the full pipeline:

1.  **Ingest Data:** Call the `ingest_s3` tool on the `dataops` server.
    `call_tool('dataops/ingest_s3', {'s3_uri': 's3://acme/churn.csv'})`

2.  **Validate Data:** Call the `validate_df` tool.
    `call_tool('dataops/validate_df', {'path': '/path/from/previous/step'})`

3.  **Feature Engineering:** Call the `encode_cat` and `impute_null` tools on the `feature` server.

4.  **Train and Evaluate:** Call the `train` and `evaluate` tools on the `trainer` server.

5.  **Deploy:** If the evaluation metrics are satisfactory (e.g., F1 score > 0.80), call the `push_k8s` tool on the `deployer` server.

### Example LLM Prompt

To trigger this entire flow, you would give a high-level prompt to a capable LLM agent:

> "Ingest `s3://acme/churn.csv`, set the target variable to `churn`, run the full pipeline, and deploy the model only if the F1 score is 0.80 or higher."

The agent would then translate this request into the sequence of tool calls described above.

---

## 5. Running Tests

The project includes a suite of unit and contract tests for each service.

1.  **Ensure dependencies are installed:**
    Make sure you have `pytest` installed from `requirements.txt`.

2.  **Run the test suite:**
    ```bash
    pytest
    ```
    This command will discover and run all tests located in the `tests/` directory.

---

## 6. Project Structure

```
├── .mcp.json            # Manifest of all MCP servers
├── docker-compose.yaml  # Defines the multi-container local stack
├── Dockerfile           # Common Docker configuration for all services
├── docs/                # Documentation files
│   ├── CLAUDE.md
│   └── GEMINI.md
├── guide.md             # This developer guide
├── README.md            # Project overview and quick-start
├── requirements.txt     # Python dependencies
├── servers/             # Source code for the MCP servers
│   ├── dataops.py
│   ├── deployer.py
│   ├── feature.py
│   └── trainer.py
├── tests/               # Unit and contract tests
│   ├── test_dataops.py
│   ├── test_deployer.py
│   ├── test_feature.py
│   └── test_trainer.py
└── workflows/           # Pipeline orchestration logic
    └── pipe.py
```
