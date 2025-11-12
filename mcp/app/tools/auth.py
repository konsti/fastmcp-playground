"""
Authentication-related demo tools.
"""

from typing import Any, override
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from fastmcp.server.dependencies import get_access_token
from app.tools.base import BaseToolProvider
from app.icons import key_square


class AuthToolProvider(BaseToolProvider):
    """
    Provider for authentication-related tools.

    This demonstrates how a class can share common authentication
    logic across multiple tools.
    """

    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)

    @override
    def register_tools(self):
        self.mcp.tool(
            name="get_token_claims",
            title="Get Token Claims",
            description="Get the JWT claims from the current access token.",
            tags={"role:all"},
            icons=[key_square],
            annotations=ToolAnnotations(
                title="Get Token Claims",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            meta={
                "unique.app/system-prompt": "Use this tool to get the JWT claims from the current access token, e.g. to determine the groups a user is a member of.",
            },
        )(self.get_token_claims)

    def get_token_claims(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        """
        Get the JWT claims from the current access token.

        Returns:
            Dictionary containing JWT claims or error message
        """
        token = get_access_token()

        if token is None:
            return {"error": "Not authenticated"}

        return token.claims or {}
