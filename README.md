# ManusAgent - Code-Server Layer

This repository contains the core configuration and startup scripts for the `code-server` component within the Manus sandbox environment.

## Contents
- `scripts/check-start-code-server.sh`: The primary startup script that handles environment pre-checks, port binding, and password generation.
- `supervisor_conf/7-code-server.conf`: The Supervisor configuration file that manages the `code-server` process lifecycle.

## Architecture
1. **systemd (PID 1)**: The system init process.
2. **supervisord (PID 699)**: Manages background services.
3. **check-start-code-server.sh**: Executed by Supervisor to initialize and run code-server.
