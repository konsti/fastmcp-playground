"""
FastMCP Playground - Entry Point

This is the main entry point for the FastMCP playground server.
"""

from app.server import create_server
from app.config.settings import settings


def main():
    """Run the FastMCP server."""
    mcp = create_server()
    mcp.run(transport="http", port=settings.port, host=settings.host)


if __name__ == "__main__":
    main()
