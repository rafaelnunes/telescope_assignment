#Telescope Assessment

## How to run
1. Clone the repository
2. Make sure you have Docker and Docker Compose installed
3. Run the following commands:

```bash
# Build  and start the application
make build

```

## Available Make Commands

- `make up`: Start all containers in detached mode
- `make down`: Stop and remove all containers
- `make create-db`: Create the initial database
- `make test`: Run tests with coverage report

## Development

The application runs on:
- Backend API: http://localhost:8000
- Database: PostgreSQL running on port 5432

## Environment Variables

The application uses a set of environment variables (configured in `.env`):

