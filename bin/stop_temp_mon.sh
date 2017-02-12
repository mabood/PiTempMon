#!/bin/sh

cd /home/pi/dev/PiTempMon/bin

ps | grep -f TMON_PID
RUNNING=$?
read -r PID <TMON_PID

if [ $RUNNING -eq 0 ]; then
   echo "Terminating TempMon..."
   set -x
   kill -STOP $PID
else
   echo "TempMon not running"
fi
