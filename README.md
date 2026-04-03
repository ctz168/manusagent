# ManusAgent - Full System Architecture

This repository contains the core configuration, startup scripts, and logic layers for the Manus autonomous agent environment.

## Architecture Layers

### 1. Interaction Layer (LLM & MCP)
- **MCP (Model Context Protocol)**: The bridge between the LLM and the sandbox tools.
  - `mcp_layer/start-manus-mcp-server.sh`: Initializes the MCP server.
  - `supervisor_conf/11-manus-mcp-server.conf`: Supervisor config for MCP.
- **Skills**: Modular "thinking templates" that guide the LLM's behavior.
  - `skills_layer/`: Contains domain-specific guidance (e.g., skill creation, music prompting).

### 2. Runtime & API Layer
- **Data API**: Internal proxy for external API calls (LLM, search, etc.).
  - `runtime_layer/data_api.py`: Python client for the internal API gateway (`api.manus.im`).
- **Environment**: Configuration via `.env` and `.user_env`.

### 3. Management & IDE Layer
- **Code-Server**: Web-based VS Code for file management.
  - `scripts/check-start-code-server.sh`: Startup and auth logic.
  - `supervisor_conf/7-code-server.conf`: Process management.

## How it works
The LLM communicates via the **MCP Server** to execute shell commands, read files, and call internal APIs through the **Runtime API Proxy**. The entire environment is orchestrated by **supervisord** and **systemd**.
