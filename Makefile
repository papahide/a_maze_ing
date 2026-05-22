PYTHON  = python3
MAIN    = a_maze_ing.py
CONFIG  = configuration.txt
UV      = uv

.PHONY: install run debug lint lint-strict build-pkg clean

install:
	@echo "Setting up environment with uv..."
	$(UV) venv
	$(UV) sync
	@echo "Done. Run: source .venv/bin/activate"

run:
	$(UV) run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(UV) run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(UV) run flake8 .
	$(UV) run mypy . --warn-return-any --warn-unused-ignores \
	                 --ignore-missing-imports \
	                 --disallow-untyped-defs \
	                 --check-untyped-defs

lint-strict:
	$(UV) run flake8 .
	$(UV) run mypy . --strict

build-pkg:
	@echo "Building mazegen package..."
	$(UV) build --out-dir .
	@echo "Package built."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .venv dist
	@echo "Cleaned."