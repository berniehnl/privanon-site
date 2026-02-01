#!/bin/bash
# Privanon Auto-Post Script
# Runs the workflow automatically via cron

# Set up paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SITE_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SCRIPT_DIR/venv"
LOG_FILE="$SCRIPT_DIR/auto_post.log"

# Timestamp for logging
echo "========================================" >> "$LOG_FILE"
echo "Auto-post started: $(date)" >> "$LOG_FILE"

# Activate virtual environment and run workflow
cd "$SITE_DIR"
source "$VENV_DIR/bin/activate"

# Run the workflow (not dry-run)
python scripts/workflow.py >> "$LOG_FILE" 2>&1

echo "Auto-post finished: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
