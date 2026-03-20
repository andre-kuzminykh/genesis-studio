#!/bin/bash
# Run the Genesis Studio Telegram bot
set -e
cd "$(dirname "$0")/.."
python -m bot.main
