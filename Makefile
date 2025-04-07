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

create-db:
	@echo "creating database if not exists...."
	docker compose exec $(DB_CONTAINER_NAME) psql -U $${POSTGRES_USER} -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$${POSTGRES_DB}'" | grep -q 1 || docker compose exec $(DB_CONTAINER_NAME) psql -U $${POSTGRES_USER} -d postgres -c "CREATE DATABASE $${POSTGRES_DB}"

alembic-migrate:
	@echo "applying migration...."
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic upgrade head

test:
	@echo "running pytest...."
	docker compose exec $(BACKEND_CONTAINER_NAME) pytest --cov-report xml --cov=app tests/

build:
	@echo "building project...."
	docker compose up -d $(DB_CONTAINER_NAME)
	@echo "waiting for database to start..."
	@sleep 5
	$(MAKE) create-db
	$(MAKE) up
	docker compose exec $(BACKEND_CONTAINER_NAME) alembic upgrade head