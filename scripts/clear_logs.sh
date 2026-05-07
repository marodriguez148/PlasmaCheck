#!/usr/bin/env bash

LOG_DIR="${1:-plasma_checker_logs}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_PATH="$SCRIPT_DIR/../$LOG_DIR"

if [ ! -d "$LOG_PATH" ]; then
    echo "Log directory not found: $LOG_PATH"
    exit 0
fi

log_files=("$LOG_PATH"/*.log)

if [ ! -e "${log_files[0]}" ]; then
    echo "No log files found in $LOG_PATH"
    exit 0
fi

echo "Found ${#log_files[@]} log file(s) in $LOG_PATH"
rm -f "${log_files[@]}"
echo "All log files removed."
