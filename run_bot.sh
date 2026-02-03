#!/bin/bash

# Script để chạy bot 24/7 với auto-restart khi crash

echo "🤖 Starting Discord Bot with auto-restart..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting bot..."
    python3 bot.py
    
    EXIT_CODE=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bot stopped with exit code: $EXIT_CODE"
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Bot stopped normally. Exiting..."
        break
    else
        echo "Bot crashed! Restarting in 5 seconds..."
        sleep 5
    fi
done
