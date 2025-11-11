# Portfolio API

A simple FastAPI service that serves portfolio data as CSV via HTTP. The service requires a JWT in the Bearer header (demo only - no validation).

## Features

- 📊 Serves portfolio data from JSON as CSV
- 🔐 JWT Bearer token authentication (demo mode - no validation)
- ⚡ Built with FastAPI and uv
- 🚀 Fast and simple

## Installation

Using uv:

```bash
cd portfolio-api
uv sync
```

## Running the Service

Start the service with:

```bash
cd portfolio-api
uv run uvicorn main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

## API Endpoints

### GET /

Returns API information and available endpoints.

```bash
curl http://localhost:8001/
```

### GET /portfolio/csv

Returns portfolio data as CSV. Requires JWT Bearer token.

**Authentication:** Bearer token (any non-empty JWT string - demo only)

**Example:**

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo.token" \
     http://localhost:8001/portfolio/csv \
     --output portfolio.csv
```

**Response:**
- Content-Type: `text/csv`
- Downloads as `portfolio-data.csv`

### GET /health

Health check endpoint.

```bash
curl http://localhost:8001/health
```

## Authentication

The service requires a JWT Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

**Note:** This is a demo implementation. The token is checked for presence but **not validated**. In production, you would validate the token signature, expiration, claims, etc.

## Development

Run with auto-reload:

```bash
uv run uvicorn main:app --reload --port 8001
```

View interactive API docs:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
portfolio-api/
├── data/
│   └── sample-data.json    # Portfolio data
├── main.py                  # FastAPI application
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```


