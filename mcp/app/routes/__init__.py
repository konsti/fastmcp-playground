"""
MCP Routes module.
"""

from fastmcp import FastMCP


def register_routes(mcp: FastMCP) -> None:
    """
    Register all custom routes with the FastMCP server.

    Args:
        mcp: The FastMCP server instance
    """
    from app.routes.health import register_health_routes

    register_health_routes(mcp)
