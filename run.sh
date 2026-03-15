#!/bin/bash

echo "Dataset Analyzer Toolbox..."

# activate virtual environment
echo "Activating Virtual Environment..."
source venv/bin/activate

# run application
echo "Running Application..."
python3 main.py

# deactivate environment after exit
echo "Deactivating Virtual Environment..."
deactivate