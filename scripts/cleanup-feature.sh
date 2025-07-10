#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <feature-branch-name>"
  exit 1
fi
git branch -d "$1"
git push origin --delete "$1"
echo "Deleted branch $1 locally and remotely." 