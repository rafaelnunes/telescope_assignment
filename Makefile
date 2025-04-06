BACKEND_CONTAINER_NAME=backend
DB_CONTAINER_NAME=db

all:

# docker
up:
	@echo "bringing up project...."
	docker compose up -d

down:
	@echo "bringing down project...."
	docker compose down

bash:
	@echo "connecting to container...."
	docker compose exec $(BACKEND_CONTAINER_NAME) bash

# alembic
alembic-scaffold:
	@echo "scaffolding migrations folder..."
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic init migrations

alembic-init:
	@echo "initializing first migration...."
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic revision --autogenerate -m "init"

alembic-make-migrations:
	@echo "creating migration file...."
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic revision --autogenerate -m "add year"

alembic-migrate:
	@echo "applying migration...."
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic upgrade head

test:
	@echo "running pytest...."
	docker compose exec $(BACKEND_CONTAINER_NAME) pytest --cov-report xml --cov=app tests/

lint:
	@echo "running ruff...."
	docker compose exec $(BACKEND_CONTAINER_NAME) ruff check .

black:
	@echo "running black...."
	docker compose exec $(BACKEND_CONTAINER_NAME) black .

mypy:
	@echo "running mypy...."
	docker compose exec $(BACKEND_CONTAINER_NAME) mypy app/

# database
init-db: alembic-init alembic-migrate
	@echo "initializing database...."
	docker compose exec $(BACKEND_CONTAINER_NAME) python3 app/db/init_db.py

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install
