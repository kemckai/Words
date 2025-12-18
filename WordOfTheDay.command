#!/bin/zsh
# Launcher for the Word of the Day sticky window.
# Uses Homebrew Python 3.11 with Tk support.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

/usr/local/opt/python@3.11/bin/python3.11 "$SCRIPT_DIR/word_of_the_day.py" &

