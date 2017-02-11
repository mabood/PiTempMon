#!/bin/sh

ps | grep -f TMON_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "TempMon already running."
    exit 1
else
    rm -rf RFManager/bin/RF_STATUS
    echo "Starting TempMon..."
    cd ../
    python lib/TempMon.py
    PID=$!
    echo $PID
    echo $PID > bin/TMON_PID
    exit 0
fi
