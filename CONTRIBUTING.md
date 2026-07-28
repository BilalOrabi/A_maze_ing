# Team Collaboration & Git Workflow Guide

Welcome to the **a-maze-ing** project! This guide outlines our branching rules, commit conventions, step-by-step feature workflows, and strategies to prevent merge conflicts while working together.

---

## 1. Branch Naming Rules

To keep the repository clean and organized, we never commit directly to `main`. Every piece of work must be done on a dedicated feature or fix branch.

### Naming Format
`<type>/<short-description>`

### Types
* `feature/` — New features, algorithms, or visualizer additions.
* `fix/` — Bug fixes or edge-case corrections.
* `refactor/` — Code cleanup or performance improvements without changing behavior.
* `docs/` — Documentation, `README.md`, or code comments.
* `test/` — Adding or updating tests.

### Examples
* `feature/dfs-generator`
* `feature/a-star-solver`
* `feature/terminal-renderer`
* `fix/config-parser-error`

---

## 2. Standard Commit Messages

Keep commit messages concise and descriptive using imperative verbs:

```bash
# Good examples
git commit -m "feat: implement Prim's maze generation algorithm"
git commit -m "fix: resolve off-by-one error in wall rendering"
git commit -m "docs: add setup instructions to README"
```

## Git Workflow & Collaboration Guide

## 3. Step-by-Step Workflow

### A. Before Starting a New Task

#### 1. Switch to `main` and pull the latest code

```bash
git checkout main
git pull origin main
```

#### 2. Create and switch to your feature branch

> Use descriptive branch names.

```bash
git checkout -b feature/your-feature-name
```

Examples:

```text
feature/dfs-generator
feature/bfs-solver
feature/config-parser
feature/render-maze
fix/input-validation
refactor/grid-structure
```

#### 3. Ensure your environment is up-to-date

```bash
poetry install
```

---

### B. While Working on Your Task

- Keep your code modular.
- Avoid modifying unrelated files.
- Follow the project's architecture.

Example module separation:

- `mazegen/generator.py` → Maze generation algorithms
- `mazegen/solver.py` → Maze solving algorithms
- `mazegen/renderer.py` → Terminal rendering
- `mazegen/config.py` → CLI/config parsing
- `mazegen/grid.py` → Grid representation

#### Run static analysis before committing

```bash
poetry run flake8
poetry run mypy mazegen
```

#### Commit your work logically

Avoid huge commits.

Good examples:

```bash
git add .
git commit -m "feat: add grid initialization"
git commit -m "feat: implement DFS maze generator"
git commit -m "fix: handle invalid maze dimensions"
git commit -m "refactor: simplify renderer logic"
```

---

### C. Finishing Your Task & Preparing to Merge

Before merging, always synchronize with the latest `main`.

#### 1. Update `main`

```bash
git checkout main
git pull origin main
```

#### 2. Return to your feature branch

```bash
git checkout feature/your-feature-name
```

#### 3. Rebase onto the latest `main`

```bash
git rebase main
```

If conflicts occur:

```bash
# Resolve conflicts manually

git add .
git rebase --continue
```

If you want to cancel the rebase:

```bash
git rebase --abort
```

#### 4. Run all checks again

```bash
poetry run flake8
poetry run mypy mazegen
```

#### 5. Push your feature branch

First push:

```bash
git push -u origin feature/your-feature-name
```

After rebasing (history changed):

```bash
git push --force-with-lease
```

> **Never use `--force`. Always use `--force-with-lease` after a rebase.**

---

# 4. How & When to Merge

## Merge only when:

- ✅ The feature is complete.
- ✅ The project builds successfully.
- ✅ `flake8` passes with zero linting errors.
- ✅ `mypy` passes with zero type errors.
- ✅ All tests pass (if applicable).
- ✅ Your teammate knows you're about to merge.

---

## Recommended: Merge via GitHub Pull Request

1. Push your branch.

```bash
git push origin feature/your-feature-name
```

2. Open a Pull Request:

```
feature/your-feature-name
        ↓
      main
```

3. Ask your teammate for a quick review.

4. Resolve any review comments.

5. Click **Squash and Merge** (recommended).

6. Delete the remote feature branch.

---

### Update your local repository

```bash
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

---

# 5. Golden Rules to Avoid Merge Conflicts

## 1. Split work by modules

Good example:

**Teammate A**

- `generator.py`
- `grid.py`

**Teammate B**

- `renderer.py`
- `config.py`

Avoid both developers editing the same file whenever possible.

---

## 2. Keep branches small

Good:

- One feature
- One bug fix
- One refactor

Bad:

- 15 unrelated changes
- 2000-line branch
- One branch open for two weeks

Small branches are easier to review and merge.

---

## 3. Communicate frequently

Examples:

> "I'm merging the parser now."

> "I just updated main."

> "Pull main before you start."

Thirty seconds of communication can save an hour of conflict resolution.

---

## 4. Pull `main` frequently

Every work session should start with:

```bash
git checkout main
git pull origin main
```

Then create (or update) your feature branch.

---

## 5. Commit Often

Don't wait until you've written 500 lines of code.

Instead:

```text
✓ Grid created
✓ DFS implemented
✓ Rendering complete
✓ CLI parsing fixed
```

Each should be its own commit.

---

## 6. Write Good Commit Messages

Use the Conventional Commits style.

Examples:

```text
feat: implement DFS maze generator
feat: add maze renderer
fix: prevent invalid grid dimensions
fix: handle empty configuration file
refactor: simplify wall removal logic
docs: update workflow guide
test: add DFS unit tests
```

---

## 7. Never Commit Generated Files or Secrets

Make sure `.gitignore` excludes things like:

```gitignore
__pycache__/
*.pyc
.mypy_cache/
.pytest_cache/
.venv/
.idea/
.vscode/
```

Never commit:

- API keys
- Passwords
- Tokens
- Local environment files (`.env`)
- Virtual environments

---

## 8. Prefer Rebase Over Merge for Feature Branches

Instead of:

```text
feature
    \
     Merge main
```

Prefer:

```bash
git rebase main
```

This keeps the Git history clean and linear.

---

# Quick Daily Workflow

```bash
# Start working
git checkout main
git pull origin main

# Create a branch
git checkout -b feature/my-feature

# Install dependencies
poetry install

# Work...

# Check formatting and typing
poetry run flake8
poetry run mypy mazegen

# Commit
git add .
git commit -m "feat: implement new feature"

# Update with latest main
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main

# Push
git push --force-with-lease

# Open Pull Request
# Review
# Squash and Merge

# Cleanup
git checkout main
git pull origin main
git branch -d feature/my-feature
```

---

# Common Mistakes to Avoid

❌ Working directly on `main`

❌ Force-pushing with `--force`

❌ Editing the same file as your teammate without communicating

❌ Keeping a feature branch alive for several days

❌ Making giant commits with unrelated changes

❌ Skipping `flake8` or `mypy` before pushing

❌ Forgetting to pull the latest `main` before starting work

❌ Rebasing shared branches that other developers are already using

❌ Committing secrets, credentials, or virtual environment files

---

# Recommended Branch Naming

```text
feature/dfs-generator
feature/prim-generator
feature/maze-renderer
feature/cli-parser

fix/input-validation
fix/render-bug

refactor/grid
refactor/generator

docs/workflow
docs/readme

test/dfs
test/renderer
```