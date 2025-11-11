"""
MCP Tools module.
"""

from fastmcp import FastMCP


def register_tools(mcp: FastMCP) -> None:
    """
    Register all tool providers with the FastMCP server.
    """
    from app.tools.auth import AuthToolProvider
    from app.tools.portfolio import PortfolioToolProvider
    from app.tools.sandbox import SandboxToolProvider

    AuthToolProvider(mcp)
    PortfolioToolProvider(mcp)
    SandboxToolProvider(mcp)
