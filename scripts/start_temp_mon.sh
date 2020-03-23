#!/bin/bash

if [ ! -f TMON_PID ]; then
    echo "INVALIDPID" > TMON_PID
fi

ps aux | grep -f TMON_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "TempMon already running."
    exit 1
else
    rm -rf TMON_PID
    echo "Starting TempMon..."
    cd ../
    python lib/TempMon.py &
    PID=$!
    echo $PID
    echo $PID > scripts/TMON_PID
    exit 0
fi