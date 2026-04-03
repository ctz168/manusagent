# Manus Agent Startup & Orchestration Guide

This guide explains how the Manus Agent environment is initialized and managed.

## 1. Orchestration Flow
The system follows a tiered startup sequence managed by `supervisord`:

1.  **Level 1: Core Runtime (`1-sandbox-runtime.conf`)**
    - The heart of the agent. It provides the API for tool execution and LLM communication.
    - Located at `/opt/.manus/.sandbox-runtime/`.
2.  **Level 2: Interaction Services**
    - **MCP Server** (`11-manus-mcp-server.conf`): The protocol bridge.
    - **WebSocket Server** (`12-ws-server.conf`): Real-time communication.
3.  **Level 3: UI & IDE Layer**
    - **Xvfb/VNC**: For headless browser and desktop interaction.
    - **Code-Server** (`7-code-server.conf`): The web IDE.

## 2. Key Orchestrator: Supervisord
Manus uses `supervisord` to ensure all components are running and healthy. 
The configuration files in `/etc/supervisor/conf.d/` (backed up in this repo) define the dependencies and restart policies.

## 3. Environment Injection
Global settings are injected via:
- `/home/ubuntu/.env`: System-generated secrets (like `CODE_SERVER_PASSWORD`).
- `/home/ubuntu/.user_env`: User-provided tokens (like `GH_TOKEN`).
- `/etc/environment`: System-wide path and resource limits.

## 4. How to Reproduce
To replicate this environment:
1.  Use the provided `Dockerfile.template`.
2.  Deploy the `supervisor_conf/` files.
3.  Ensure the startup scripts in `scripts/` and `mcp_layer/` are executable.
