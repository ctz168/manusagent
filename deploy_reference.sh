#!/bin/bash
# ManusAgent Deployment Reference Script
# This script demonstrates how to set up the agent environment from this repository.

set -e

echo "Starting ManusAgent environment setup..."

# 1. Directory Setup
echo "Creating directory structure..."
sudo mkdir -p /opt/.manus/.packages/scripts
sudo mkdir -p /etc/supervisor/conf.d
sudo mkdir -p /home/ubuntu/skills
sudo mkdir -p /home/ubuntu/.config/code-server

# 2. Deploy Scripts
echo "Deploying startup scripts..."
sudo cp scripts/check-start-code-server.sh /opt/.manus/.packages/scripts/
sudo cp mcp_layer/start-manus-mcp-server.sh /opt/.manus/.packages/scripts/
sudo chmod +x /opt/.manus/.packages/scripts/*.sh

# 3. Deploy Supervisor Configs
echo "Deploying Supervisor configurations..."
sudo cp supervisor_conf/*.conf /etc/supervisor/conf.d/

# 4. Deploy Skills
echo "Deploying Agent Skills..."
cp -r skills_layer/* /home/ubuntu/skills/

# 5. Runtime API Setup
echo "Deploying Runtime API client..."
mkdir -p /opt/.manus/current
cp runtime_layer/data_api.py /opt/.manus/current/

# 6. Environment Variables
echo "Initializing environment variables..."
if [ ! -f /home/ubuntu/.env ]; then
    cat <<EOF > /home/ubuntu/.env
export APP_ENV=PROD
export RUNTIME_API_HOST=https://api.manus.im
export TZ=UTC
EOF
fi

# 7. Start Services
echo "Reloading Supervisor..."
# In a real environment, you would run:
# sudo supervisorctl reread
# sudo supervisorctl update
# sudo supervisorctl start all

echo "-------------------------------------------------------"
echo "ManusAgent environment deployment reference completed."
echo "Note: This is a reference script. Ensure you have"
echo "installed all dependencies from Dockerfile.template."
echo "-------------------------------------------------------"
