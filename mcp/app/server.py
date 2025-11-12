"""
FastMCP server instance and configuration.
"""

from fastmcp import FastMCP
from app.auth.setup import setup_auth
from app.middleware import AuthorizationMiddleware, RoleBasedVerifier


def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server instance.

    Returns:
        FastMCP: Configured FastMCP server instance
    """
    auth_provider = setup_auth()
    mcp = FastMCP(
        name="FastMCP Playground",
        auth=auth_provider,
        include_fastmcp_meta=False,
    )

    mcp.add_middleware(AuthorizationMiddleware(RoleBasedVerifier()))

    from app.tools import register_tools
    from app.routes import register_routes
    from app.resources import register_resources

    register_tools(mcp)
    register_routes(mcp)
    register_resources(mcp)

    return mcp
