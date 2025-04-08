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


## Client Scripts

Inside the `resources/client` directory, there are Python scripts to interact with the API endpoints:

### Import Company Data
To import company data from CSV or JSON files:

```bash
# Using the default CSV file in resources directory
./resources/client/import_companies.py

# Or specify a custom CSV file path
./resources/client/import_companies.py /path/to/your/file.csv
```

### Process Companies
To process companies using rules from a JSON file:

```bash
# Using the default rules.json file in resources directory
./resources/client/process_companies.py

# Or specify a custom rules file path
./resources/client/process_companies.py /path/to/your/rules.json
```

### Get Companies
To retrieve companies from the database:

```bash
# Get all companies
./resources/client/get_companies.py

# Get companies with filters (as JSON string)
./resources/client/get_companies.py '{"is_saas": true}'
```

### Requirements
The client scripts require the `requests` package. Install it with:

```bash
pip install requests
```

Make sure the FastAPI server is running on `localhost:8000` before using these scripts.
