# Git Workflow Scripts

This directory contains helper scripts for managing a best-practice Git workflow with feature branches, releases, and versioning.

## Scripts

### `start-feature.sh <branch-name>`
Creates a new feature branch from the latest main branch.
```bash
./scripts/start-feature.sh my-new-feature
```

### `commit-feature.sh <message>`
Commits all staged changes and pushes to the current feature branch.
```bash
./scripts/commit-feature.sh "feat: add new LLM provider"
```

### `prepare-release.sh <version>`
Merges the current feature branch to main, bumps version, tags, and pushes.
```bash
./scripts/prepare-release.sh 1.2.0
```

### `cleanup-feature.sh <branch-name>`
Deletes the feature branch locally and remotely after merge.
```bash
./scripts/cleanup-feature.sh my-new-feature
```

## Workflow Example

```bash
# 1. Start a new feature
./scripts/start-feature.sh add-ollama-support

# 2. Make changes and commit
./scripts/commit-feature.sh "feat: add Ollama provider"

# 3. When ready to release
./scripts/prepare-release.sh 1.2.0

# 4. Clean up the feature branch
./scripts/cleanup-feature.sh add-ollama-support
```

## Notes

- These scripts are not committed to the repository (see `.gitignore`)
- Always work on feature branches, never directly on main
- Use conventional commit messages (feat:, fix:, chore:, etc.)
- Version bumps are automatic in `pyproject.toml` if present 