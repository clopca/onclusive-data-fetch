#!/bin/bash
# Script para ejecutar con cron

cd "$(dirname "$0")"

# Load env vars
export $(grep -v '^#' .env | xargs)

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run
python fetch_selenium.py

# Log
echo "Execution completed at $(date)" >> cron.log

