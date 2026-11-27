#!/bin/bash
# Restores the carousel pipeline to the absolute paths the scripts expect.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /home/claude/carousel /home/claude/fonts /home/claude/book/assets
cp "$D"/carousel/* /home/claude/carousel/
cp "$D"/fonts/* /home/claude/fonts/
cp "$D"/book_assets/* /home/claude/book/assets/
python3 -c "import PIL" 2>/dev/null || pip install --break-system-packages -q pillow
echo "pipeline ready in /home/claude/carousel"
