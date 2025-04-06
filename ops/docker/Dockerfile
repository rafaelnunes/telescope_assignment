FROM python:3.12 AS base

ARG env

WORKDIR /tmp

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry>=2.0.1"

COPY pyproject.toml poetry.lock* ./

# Install dependencies and explicitly install psycopg2-binary
RUN poetry config virtualenvs.create false \
    && poetry install --no-root $(test "${env:-dev}" != "prod" && echo "--with dev") \
    && pip install psycopg2-binary==2.9.10 \
    && poetry run pip freeze > requirements.txt

FROM python:3.12

# Install system dependencies in the final image
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=base /tmp/requirements.txt /app/requirements.txt

# Install dependencies and explicitly install psycopg2-binary
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && pip install --no-cache-dir psycopg2-binary==2.9.10

WORKDIR /app
COPY . /app/

ENV PYTHONPATH=/app

# Verify psycopg2 installation
RUN python -c "import psycopg2; print(f'psycopg2 version: {psycopg2.__version__}')"

EXPOSE 8000
