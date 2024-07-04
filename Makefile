.PHONY: help copy-envs setup install requirements pre-commit safety run-local test clean

PROJECT_NAME := fms-vpo

help:
	@printf "A set of development commands.\n"
	@printf "\nUsage:\n"
	@printf "\t make \033[36m<commands>\033[0m\n"
	@printf "\nThe Commands are:\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2}'

copy-envs:
	@cp -n .example.secrets.toml .secrets.toml

setup:
	poetry shell

install:
	poetry install --no-root

install-new-dependencies:
	poetry lock --no-update
	poetry install --no-root

pre-commit:
	poetry run pre-commit run -a

run:
	poetry run python main.py

db-up:
	poetry run alembic upgrade head

db-down:
	poetry run alembic downgrade -1

test:
	poetry run pytest -vv

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .coverage
	rm -rf  coverage_html
	rm -rf .pytest_cache
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	rm -rf celerybeat-schedule
	rm -rf *.pyc
	rm -rf *__pycache__
	rm -rf .mypy_cache

build-dev:
	docker build . -t fms-vpo -f k8s/Dockerfile

redis-dev:
	docker run --name redisdev -p 6379:6379 -d redis
