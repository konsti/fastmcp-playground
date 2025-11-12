"""
Health check routes for the FastMCP server.
"""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse


def register_health_routes(mcp: FastMCP) -> None:
    """
    Register health check routes.
    """

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> PlainTextResponse:  # pyright: ignore[reportUnusedFunction]
        """
        Health check endpoint to verify server is running.
        """
        return PlainTextResponse("OK")
