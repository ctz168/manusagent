# ManusAgent - Full System Architecture & Build Guide

This repository contains the core configuration, startup scripts, and logic layers for the Manus autonomous agent environment.

## Architecture Layers

### 1. Build & Orchestration Layer (New!)
- **Dockerfile Template**: Inferred build instructions for the Ubuntu 22.04 sandbox.
- **Startup Guide**: Detailed explanation of the `supervisord` orchestration sequence.
- See `build_layer/`.

### 2. Interaction Layer (LLM & MCP)
- **MCP (Model Context Protocol)**: The bridge between the LLM and the sandbox tools.
- **Skills**: Modular "thinking templates" that guide the LLM's behavior.
- See `mcp_layer/` and `skills_layer/`.

### 3. Runtime & API Layer
- **Data API**: Internal proxy for external API calls (LLM, search, etc.).
- See `runtime_layer/`.

### 4. Management & IDE Layer
- **Code-Server**: Web-based VS Code for file management.
- See `scripts/` and `supervisor_conf/`.

## Summary
Manus is a highly orchestrated Linux environment where an LLM (the Brain) uses the MCP Server (the Nervous System) to control a set of specialized tools and runtimes (the Body), all managed by Supervisor (the Vital Signs Monitor).
