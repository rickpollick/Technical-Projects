#!/bin/bash

# Your Python script's path
PYTHON_SCRIPT_PATH=""

# Reference Date: April 3, 2024 (YYYY-MM-DD)
REFERENCE_DATE=""

# Calculate weeks since reference date
WEEKS_SINCE=$(($(($(date +%s) - $(date -jf "%Y-%m-%d" "$REFERENCE_DATE" +%s)) / 86400) / 7))

# Check if weeks since is an even number - indicating a bi-weekly schedule
if [ $((WEEKS_SINCE % 2)) -eq 0 ]; then
  # Run Python script
  python3 "$PYTHON_SCRIPT_PATH"
fi

# This can also be achieved by setting up a cron job or a launchd task with the appropriate timing.
