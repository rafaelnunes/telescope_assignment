<p align="center">
    <a href="https://github.com/rafaelnunes/core-saida-orchestrator/actions">
        <img alt="GitHub Actions status" src="https://github.com/rafaelnunes/core-saida-orchestrator/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://github.com/rafaelnunes/core-saida-orchestrator/releases"><img alt="Release Status" src="https://img.shields.io/github/v/release/rafaelnunes/core-saida-orchestrator"></a>
</p>

# core-saida-orchestrator

## Architecture

<p align="center">
    <a href="#">
        <img alt="Architecture Workflow" src="https://i.imgur.com/8TEpVZk.png">
    </a>
</p>

## Usage

1. `make up`
2. visit `http://localhost:8666/v1/ping` for uvicorn server, or `http://localhost` for nginx server
3. Backend, JSON based web API based on OpenAPI: `http://localhost/v1/`
4. Automatic interactive documentation with Swagger UI (from the OpenAPI backend): `http://localhost/docs`

## Backend local development, additional details

Initialize first migration (project must be up with docker compose up and contain no 'version' files)

```shell
$ make alembic-init
```

Create new migration file

```shell
$ docker compose exec backend alembic revision --autogenerate -m "some cool comment"
```

Apply migrations

```shell
$ make alembic-migrate
```

### Migrations

Every migration after that, you can create new migrations and apply them with

```console
$ make alembic-make-migrations "cool comment dude"
$ make alembic-migrate
```

### General workflow

See the [Makefile](/Makefile) to view available commands.

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ poetry install
```

### pre-commit hooks

If you haven't already done so, download [pre-commit](https://pre-commit.com/) system package and install. Once done, install the git hooks with

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Some of the environment variables available:

- `UPSTREAMS=/:backend:8000` a comma separated list of \<path\>:\<upstream\>:\<port\>. Each of those of those elements creates a location block with proxy_pass in it.

### Deployments

A common scenario is to use an orchestration tool, such as docker swarm, to deploy your containers to the cloud (DigitalOcean). This can be automated via GitHub Actions workflow. See [main.yml](/.github/workflows/main.yml) for more.

You will be required to add `secrets` in your repo settings:

- DIGITALOCEAN_TOKEN: your DigitalOcean api token
- REGISTRY: container registry url where your images are hosted
- POSTGRES_PASSWORD: password to postgres database
- STAGING_HOST_IP: ip address of the staging droplet
- PROD_HOST_IP: ip address of the production droplet
- SSH_KEY: ssh key of user connecting to server (`ubuntu` in this case)
