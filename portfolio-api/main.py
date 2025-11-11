"""
FastAPI service to serve portfolio data as CSV.
Requires JWT Bearer token (demo - no validation).
"""

import csv
import io
import json
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import StreamingResponse

app = FastAPI(title="Portfolio API", version="0.1.0")

# Path to the sample data
DATA_FILE = Path(__file__).parent / "data" / "sample-data.json"


def load_portfolio_data() -> list[dict]:
    """Load portfolio data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def check_jwt_bearer(authorization: str | None) -> None:
    """
    Check if JWT Bearer token is present.
    Demo only - does not validate the token.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Expected 'Bearer'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Demo: We don't validate the token, just check it exists


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Portfolio API",
        "version": "0.1.0",
        "description": "Serves portfolio data as CSV",
        "endpoints": {
            "/portfolio/csv": "Get portfolio data as CSV (requires JWT Bearer token)"
        },
    }


@app.get("/portfolio/csv")
async def get_portfolio_csv(authorization: Annotated[str | None, Header()] = None):
    """
    Get portfolio data as CSV.

    Requires a JWT Bearer token in the Authorization header.
    Token is not validated (demo only).
    """
    # Check for JWT Bearer token (demo - no validation)
    check_jwt_bearer(authorization)

    # Load portfolio data
    data = load_portfolio_data()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No portfolio data available"
        )

    # Create CSV in memory
    output = io.StringIO()

    # Get all field names from the first record
    fieldnames = list(data[0].keys())

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    # Get CSV content
    csv_content = output.getvalue()

    # Return as streaming response
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=portfolio-data.csv"},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
