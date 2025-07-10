#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <new-version> (e.g. 1.2.0)"
  exit 1
fi
NEW_VERSION="$1"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "You are already on main. Please run this from your feature branch."
  exit 1
fi
git checkout main
git pull origin main
git merge --no-ff "$CURRENT_BRANCH" -m "Merge $CURRENT_BRANCH for release $NEW_VERSION"
if [ -f pyproject.toml ]; then
  sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
  git add pyproject.toml
  git commit -m "chore: bump version to $NEW_VERSION"
fi
git push origin main
git tag "v$NEW_VERSION"
git push origin "v$NEW_VERSION"
echo "Release $NEW_VERSION is now on main and tagged." 