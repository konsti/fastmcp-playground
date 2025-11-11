"""
FastMCP server instance and configuration.
"""

from fastmcp import FastMCP
from app.auth.setup import setup_auth


def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server instance.
    
    Returns:
        FastMCP: Configured FastMCP server instance
    """
    auth_provider = setup_auth()
    mcp = FastMCP("FastMCP Playground", auth=auth_provider)
    
    from app.tools import register_tools
    register_tools(mcp)
    
    return mcp
