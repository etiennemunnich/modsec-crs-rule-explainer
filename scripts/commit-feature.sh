#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <commit-message>"
  exit 1
fi
git add .
git commit -m "$1"
git push -u origin $(git rev-parse --abbrev-ref HEAD)
echo "Committed and pushed to branch: $(git rev-parse --abbrev-ref HEAD)" 