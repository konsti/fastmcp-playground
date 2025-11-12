"""
Authorization middleware for role-based access control.

This middleware checks JWT claims to control access to tools based on user permissions.
Can be configured with custom verifier classes to implement any authorization logic.
"""

from abc import ABC, abstractmethod
from typing import Any, override
from fastmcp.tools.tool import Tool
from pydantic import BaseModel, Field
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_access_token


class ToolVerifier(BaseModel, ABC):  # pyright: ignore[reportUnsafeMultipleInheritance]
    """
    Base class for tool authorization verifiers.

    Verifiers determine whether users can access specific tools based on
    their JWT claims. Subclass this to implement custom authorization logic.

    Example:
        ```python
        class CustomVerifier(ToolVerifier):
            allowed_users: list[str] = []

            async def verify(self, claims: dict[str, Any], tool: Tool) -> bool:
                user_id = claims.get("sub")
                return user_id in self.allowed_users

        middleware = AuthorizationMiddleware(
            verifier=CustomVerifier(allowed_users=["user1", "user2"])
        )
        ```
    """

    model_config = {"arbitrary_types_allowed": True}

    @abstractmethod
    async def verify(self, claims: dict[str, Any], tool: Tool) -> bool:  # pyright: ignore[reportExplicitAny]
        """
        Verify if the user has access to the tool.

        Args:
            claims: User claims from the access token
            tool: The tool being accessed

        Returns:
            True if access is granted, False otherwise
        """
        ...


class RoleBasedVerifier(ToolVerifier):
    """
    Role-based access control verifier.
    """

    claims_path: str = Field(
        default="realm_access.roles",
        description="Path to roles in JWT claims (dot-separated)",
    )
    allow_no_role_tags: bool = Field(
        default=False, description="Allow access to tools without role tags"
    )

    def _extract_roles(self, claims: dict[str, Any]) -> set[str]:  # pyright: ignore[reportExplicitAny]
        """
        Extract user roles from JWT claims using the configured path.
        """
        parts = self.claims_path.split(".")
        current = claims

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part, [])  # pyright: ignore[reportAny]
            else:
                return set()

        if isinstance(current, list):
            return set(current)  # pyright: ignore[reportUnknownArgumentType]
        return set()

    @override
    async def verify(self, claims: dict[str, Any], tool: Tool) -> bool:  # pyright: ignore[reportExplicitAny]
        user_roles = self._extract_roles(claims)
        tool_tags = getattr(tool, "tags", [])

        if "role:all" in tool_tags:
            return True

        role_tags = [tag for tag in tool_tags if tag.startswith("role:")]  # pyright: ignore[reportAny]

        if not role_tags:
            return self.allow_no_role_tags

        for tag in role_tags:  # pyright: ignore[reportAny]
            required_role: str = tag[5:]  # pyright: ignore[reportAny]
            if required_role in user_roles:
                return True

        return False


class ScopeBasedVerifier(ToolVerifier):
    """
    Scope-based access control verifier.

    Checks tool tags with 'scope:' prefix against JWT scopes/permissions.
    Common for OAuth2/OIDC token-based authorization.

    Args:
        claims_path: Path to scopes in claims. Defaults to 'scope' (standard OAuth2).
                     Can be 'scopes' or custom path.
        allow_no_scope_tags: Whether to allow access when tool has no scope tags.
                            Defaults to False for secure-by-default behavior.

    Example:
        ```python
        # Standard OAuth2 scopes
        verifier = ScopeBasedVerifier()

        # Custom claims path
        verifier = ScopeBasedVerifier(claims_path="permissions")

        # Tool definition
        @mcp.tool(tags=["scope:read:data", "scope:write:data"])
        async def process_data():
            pass
        ```
    """

    claims_path: str = Field(
        default="scope", description="Path to scopes in JWT claims"
    )
    allow_no_scope_tags: bool = Field(
        default=False, description="Allow access to tools without scope tags"
    )

    def _extract_scopes(self, claims: dict[str, Any]) -> set[str]:  # pyright: ignore[reportExplicitAny]
        parts = self.claims_path.split(".")
        current = claims

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part, "")  # pyright: ignore[reportAny]
            else:
                return set()

        if isinstance(current, str):
            return set(current.split()) if current else set()
        elif isinstance(current, list):
            return set(current)  # pyright: ignore[reportUnknownArgumentType]
        return set()

    @override
    async def verify(self, claims: dict[str, Any], tool: Tool) -> bool:  # pyright: ignore[reportExplicitAny]
        user_scopes = self._extract_scopes(claims)
        tool_tags = getattr(tool, "tags", [])

        scope_tags = [tag for tag in tool_tags if tag.startswith("scope:")]  # pyright: ignore[reportAny]

        if not scope_tags:
            return self.allow_no_scope_tags

        # Check if user has ALL required scopes (AND logic)
        required_scopes: list[str] = [
            tag[6:]
            for tag in scope_tags  # pyright: ignore[reportAny]
        ]
        return all(scope in user_scopes for scope in required_scopes)


class AuthorizationMiddleware(Middleware):
    """
    Configurable authorization middleware for tool access control.

    Accepts a ToolVerifier instance that determines whether users can access specific tools
    based on their JWT claims. The verifier is called for both tool listing (filtering)
    and tool execution (validation).

    Args:
        verifier: ToolVerifier instance for authorization logic.
    """

    def __init__(self, verifier: ToolVerifier):
        super().__init__()
        self.verifier = verifier

    def _get_claims(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        token = get_access_token()

        if token is None:
            return {}

        return token.claims

    @override
    async def on_list_tools(self, context: MiddlewareContext, call_next):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        """
        Filter tool listings based on user permissions.

        Only returns tools that the user has access to according to the verifier.
        """
        claims = self._get_claims()
        result = await call_next(context)

        # Filter tools based on verifier
        filtered_tools = []
        for tool in result:
            if await self.verifier.verify(claims, tool):
                filtered_tools.append(tool)  # pyright: ignore[reportUnknownMemberType]

        return filtered_tools  # pyright: ignore[reportUnknownVariableType]

    @override
    async def on_call_tool(self, context: MiddlewareContext, call_next):  # pyright: ignore[reportMissingParameterType]
        """
        Validate tool execution permissions before allowing tool calls.

        Checks if user has permission to execute the requested tool.
        Raises ToolError if access is denied.
        """
        if context.fastmcp_context:
            try:
                tool = await context.fastmcp_context.fastmcp.get_tool(
                    context.message.name  # pyright: ignore[reportAny]
                )

                if not tool.enabled:
                    raise ToolError("Tool is currently disabled")

                claims = self._get_claims()
                has_access = await self.verifier.verify(claims, tool)

                if not has_access:
                    raise ToolError(
                        "Access denied. You do not have permission to execute this tool."
                    )

            except ToolError:
                raise
            except Exception:
                # Tool not found or other error - let execution continue
                # and handle the error naturally
                pass

        return await call_next(context)
