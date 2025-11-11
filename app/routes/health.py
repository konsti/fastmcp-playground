"""
Health check routes for the FastMCP server.
"""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse


def register_health_routes(mcp: FastMCP) -> None:
    """
    Register health check routes.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> PlainTextResponse:
        """
        Health check endpoint to verify server is running.
        
        Returns:
            PlainTextResponse: "OK" status
        """
        return PlainTextResponse("OK")

