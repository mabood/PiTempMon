#!/bin/sh

cd /home/pi/dev/PiTempMon/bin

ps aux | grep -f TMON_PID
RUNNING=$?
read -r PID <TMON_PID

if [ $RUNNING -eq 0 ];
then
   echo "Terminating TempMon..."
   kill -9 $PID
   exit 0
else
   echo "TempMon not running"
   exit 1
fi


