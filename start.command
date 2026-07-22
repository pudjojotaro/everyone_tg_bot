#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 was not found on this Mac."
    echo "Install it from https://www.python.org/downloads/ then double-click this file again."
    read -p "Press Enter to close..."
    exit 1
fi

if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

if [ ! -f .env ]; then
    echo ""
    echo "First-time setup: paste your bot token from @BotFather below."
    read -p "Bot token: " BOT_TOKEN
    echo "BOT_TOKEN=$BOT_TOKEN" > .env
fi

echo ""
echo "Starting the bot... (Ctrl+C or close this window to stop it)"
python bot.py

read -p "Press Enter to close..."
