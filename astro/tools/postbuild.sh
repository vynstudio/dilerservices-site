#!/bin/bash
# Copy legacy static ES/PT pages, thanks pages and their assets into dist, then build purged CSS.
set -e
cd "$(dirname "$0")/.."
cp -rn ../finclix/. dist/ 2>/dev/null || true
rm -f dist/fonts/*.html
python3 tools/build_css.py
