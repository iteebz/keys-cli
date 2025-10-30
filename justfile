default:
    @just --list

clean:
    @echo "Cleaning keys..."
    @rm -rf dist build .pytest_cache .ruff_cache __pycache__ .venv
    @find . -type d -name "__pycache__" -exec rm -rf {} +

install:
    @poetry lock
    @poetry install

ci:
    @poetry run ruff format .
    @poetry run ruff check . --fix --unsafe-fixes
    @poetry run pytest tests -q
    @poetry build

test:
    @poetry run pytest tests -q

run:
    @poetry run keys

format:
    @poetry run ruff format .

lint:
    @poetry run ruff check .

fix:
    @poetry run ruff check . --fix --unsafe-fixes

build:
    @poetry build

repomix:
    repomix

commits:
    @git --no-pager log --pretty=format:"%h | %ar | %s"
