"""
MCP Tools module.
"""

from fastmcp import FastMCP


def register_tools(mcp: FastMCP) -> None:
    """
    Register all tool providers with the FastMCP server.

    Tool providers are classes that encapsulate related tools and register
    them during initialization.
    """
    from app.tools.basic import BasicToolProvider
    from app.tools.auth import AuthToolProvider
    from app.tools.portfolio import PortfolioToolProvider

    BasicToolProvider(mcp)
    AuthToolProvider(mcp)
    PortfolioToolProvider(mcp)
