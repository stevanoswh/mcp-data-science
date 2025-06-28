# mcp-ml-e2e

This project provides a single-command, end-to-end ML engineering pipeline that an LLM agent can run through Model Context Protocol (MCP) calls. The goal is to automate the process from raw data ingestion to model deployment and monitoring.

The pipeline consists of four main services, each running as a separate MCP server:
- **DataOps:** Handles data ingestion and validation.
- **Feature:** Performs feature engineering tasks like encoding and imputation.
- **Trainer:** Trains and evaluates the machine learning model.
- **Deployer:** Deploys the trained model to a Kubernetes-like environment and monitors for drift.

For a complete guide on how to set up, run, and interact with this project, please refer to the [Developer Guide](guide.md).