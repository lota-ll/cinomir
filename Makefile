.DEFAULT_GOAL := help
PY ?= python3
VENV := .venv
BIN := $(VENV)/bin
Q ?= тунець у власному соку
ARGS ?=

.PHONY: help env install lint fmt test up up-bot down clean logs search

help: ## Показати команди
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

env: ## Створити .env з .env.example (не перезаписує)
	@test -f .env || cp .env.example .env && echo ".env готовий"

$(BIN)/activate:
	$(PY) -m venv $(VENV)

install: $(BIN)/activate ## Віртуальне оточення + залежності + pre-commit
	$(BIN)/pip install -e ".[dev]"
	$(BIN)/pre-commit install

lint: ## ruff: помилки + форматування
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

fmt: ## Автоформатування
	$(BIN)/ruff check --fix .
	$(BIN)/ruff format .

test: ## Тести (без Docker і без мережі)
	$(BIN)/pytest

up: env ## Запустити стек (працюватиме після задачі 6)
	docker compose up -d --build --wait

up-bot: env ## Стек + бот (після задачі 6)
	docker compose --profile bot up -d --build

down: ## Зупинити (дані БД лишаються)
	docker compose --profile bot down

clean: ## Зупинити і видалити дані БД
	docker compose --profile bot down -v

logs: ## Логи всіх сервісів
	docker compose --profile bot logs -f --tail=100

search: ## Пошук через API (після задачі 5)
	$(BIN)/cinomir-search "$(Q)" $(ARGS)
