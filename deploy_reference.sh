#!/bin/bash
# ManusAgent Deployment Reference Script
# This script demonstrates how to set up the agent environment from this repository.

set -e

# Base directory for deployment (Default is system root, can be overridden for testing)
BASE_DIR=${1:-"/"}

echo "Starting ManusAgent environment setup in ${BASE_DIR}..."

# 1. Directory Setup
echo "Creating directory structure..."
mkdir -p "${BASE_DIR}/opt/.manus/.packages/scripts"
mkdir -p "${BASE_DIR}/opt/.manus/.sandbox-runtime"
mkdir -p "${BASE_DIR}/etc/supervisor/conf.d"
mkdir -p "${BASE_DIR}/home/ubuntu/skills"
mkdir -p "${BASE_DIR}/home/ubuntu/.config/code-server"

# 2. Deploy Scripts
echo "Deploying startup scripts..."
cp scripts/check-start-code-server.sh "${BASE_DIR}/opt/.manus/.packages/scripts/"
cp mcp_layer/start-manus-mcp-server.sh "${BASE_DIR}/opt/.manus/.packages/scripts/"
chmod +x "${BASE_DIR}/opt/.manus/.packages/scripts/"*.sh

# 3. Deploy Supervisor Configs
echo "Deploying Supervisor configurations..."
cp supervisor_conf/*.conf "${BASE_DIR}/etc/supervisor/conf.d/"

# 4. Deploy Skills
echo "Deploying Agent Skills..."
cp -r skills_layer/* "${BASE_DIR}/home/ubuntu/skills/"

# 5. Environment Variables
echo "Initializing environment variables..."
if [ ! -f "${BASE_DIR}/home/ubuntu/.env" ]; then
    cat <<EOF > "${BASE_DIR}/home/ubuntu/.env"
export APP_ENV=PROD
export RUNTIME_API_HOST=https://api.manus.im
export TZ=UTC
EOF
fi

echo "-------------------------------------------------------"
echo "ManusAgent environment deployment reference completed."
echo "Note: This is a reference script. Ensure you have"
echo "installed all dependencies from Dockerfile.template."
echo "-------------------------------------------------------"
