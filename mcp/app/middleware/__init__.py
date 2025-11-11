"""
Middleware module for FastMCP server.
"""

from app.middleware.authorization import AuthorizationMiddleware

__all__ = ["AuthorizationMiddleware"]

