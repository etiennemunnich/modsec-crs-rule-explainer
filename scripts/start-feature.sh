#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <feature-branch-name>"
  exit 1
fi
git checkout main
git pull origin main
git checkout -b "$1"
echo "Switched to new branch: $1" 