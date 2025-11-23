#!/bin/bash
# Launch or reattach to a named screen session

SESSION="SESSION_NAME"
CMD="PATH/TO/PROGRAM"

# Check if screen session exists
if screen -list | grep -q "[.]${SESSION}[[:space:]]"; then
    echo "Reattaching to existing screen session: $SESSION"
    screen -dr "$SESSION"
else
    echo "Starting new screen session: $SESSION"
    screen -S "$SESSION" bash -c "sudo $CMD"
fi
