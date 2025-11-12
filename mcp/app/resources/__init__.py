"""
MCP Resources module.
"""

from fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """
    Register all resource providers with the FastMCP server.
    """
    from app.resources.portfolio import PortfolioResourceProvider

    PortfolioResourceProvider(mcp)