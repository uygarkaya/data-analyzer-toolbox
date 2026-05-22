#!/bin/bash
set -e

echo "Dataset Analyzer Toolbox - Setup"

if [ ! -d "venv" ]; then
    echo "Creating Virtual Environment: 'venv'"
    python3.11 -m venv venv
else
    echo "Virtual Environment 'venv' Already Exists, Skipping Creation!"
fi

echo "Activating Virtual Environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Dependencies From requirements-dev.txt..."
pip install -r requirements-dev.txt

if [ ! -f ".env" ]; then
    echo "Creating .env File..."
    cat > .env <<EOF
DATASET_URL="configuration/assets/datasets.json"
MODELS_URL="configuration/assets/models.json"
HOST="localhost"
PORT="8050"
EOF
else
    echo ".env File Already Exists, Skipping Creation!"
fi

chmod +x run.sh

echo ""
echo "Setup Complete. Run the app with: ./run.sh"
