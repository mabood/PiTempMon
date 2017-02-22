#!/bin/sh

cd /home/pi/dev/PiTempMon/bin

if [ ! -f NODE_PID ]; then
    echo "INVALIDPID" > NODE_PID
fi

ps aux | grep -f NODE_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "TempMon already running."
    exit 1
else
    rm -rf NODE_PID
    echo "Starting Node Server..."
    cd ../node/
    node server.js &
    PID=$!
    echo $PID
    echo $PID > ../bin/NODE_PID
    exit 0
fi