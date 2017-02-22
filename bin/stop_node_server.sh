#!/bin/sh

cd /home/pi/dev/PiTempMon/bin

ps aux | grep -f NODE_PID
RUNNING=$?
read -r PID <NODE_PID

if [ $RUNNING -eq 0 ];
then
   echo "Terminating Node Server..."
   kill -9 $PID
   exit 0
else
   echo "Node Server not running."
   exit 1
fi


