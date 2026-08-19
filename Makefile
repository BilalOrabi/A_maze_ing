# ==============================================================================
# A-Maze-ing Project Makefile
# ==============================================================================

# Variables
PYTHON      := poetry run python
PYTEST      := poetry run pytest
MYPY        := poetry run mypy
FLAKE8      := poetry run flake8 --count
MAIN_SCRIPT := a_maze_ing.py
CONFIG_FILE := config.txt

.PHONY: all install run test debug clean lint build help

all: install lint test build

install:
	@echo "==> Installing dependencies..."
	poetry install

## Run the main application
run:
	@echo "==> Running A-Maze-ing..."
	@if [ -f $(CONFIG_FILE) ]; then \
		$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE); \
	else \
		$(PYTHON) $(MAIN_SCRIPT); \
	fi

## Run unit tests and coverage analysis
test:
	@echo "==> Running pytest with detailed coverage..."
	$(PYTEST) -v --cov=mazegen --cov=app --cov-report=term-missing

## Run main script in debug mode using pdb (As required by subject page 7)
debug:
	@echo "==> Running main script in debug mode (pdb)..."
	@if [ -f $(CONFIG_FILE) ]; then \
		$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE); \
	else \
		$(PYTHON) -m pdb $(MAIN_SCRIPT); \
	fi

clean:
	@echo "==> Cleaning cache and build artifacts..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	@echo "==> Running MyPy type checker..."
	$(MYPY) mazegen app $(MAIN_SCRIPT)
	@echo "==> Running Flake8 linter..."
	$(FLAKE8) mazegen app $(MAIN_SCRIPT)

build:
	@echo "==> Building package with Poetry..."
	poetry build
	@cp dist/*.whl . 2>/dev/null || true
	@echo "==> Built wheel package placed at root."

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install   Install dependencies via Poetry"
	@echo "  run       Execute main application (a_maze_ing.py)"
	@echo "  test      Run unit tests with pytest coverage analysis"
	@echo "  debug     Run a_maze_ing.py with pdb interactive debugger"
	@echo "  lint      Run MyPy and Flake8 code quality checks"
	@echo "  build     Build wheel (.whl) package using Poetry"
	@echo "  clean     Remove temporary files, caches, and build folders"