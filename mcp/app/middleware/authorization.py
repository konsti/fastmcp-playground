"""
Authorization middleware for role-based access control.

This middleware checks JWT claims to control access to tools based on user roles.
"""

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_access_token


class AuthorizationMiddleware(Middleware):
    """
    Authorization middleware that enforces role-based access control on tools.
    """
    
    def _get_user_roles(self) -> set[str]:
        """
        Extract user roles from JWT token claims.
        """
        token = get_access_token()
        
        if token is None:
            return set()
        
        realm_access = token.claims.get("realm_access", {})
        roles = realm_access.get("roles", [])
        
        return set(roles)
    
    def _has_access_to_tool(self, tool_tags: list[str], user_roles: set[str]) -> bool:
        """
        Check if user has access to a tool based on tags and roles.
        """
        if "role:all" in tool_tags:
            return True
        
        for tag in tool_tags:
            if tag.startswith("role:"):
                required_role = tag[5:]
                if required_role in user_roles:
                    return True
        
        return False
    
    async def on_list_tools(self, context: MiddlewareContext, call_next):
        """
        Filter tool listings based on user roles.
        """
        user_roles = self._get_user_roles()
        result = await call_next(context)
        
        filtered_tools = [
            tool for tool in result
            if self._has_access_to_tool(getattr(tool, "tags", []), user_roles)
        ]

        return filtered_tools
    
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """
        Validate tool execution permissions before allowing tool calls.
        """
        if context.fastmcp_context:
            try:
                tool = await context.fastmcp_context.fastmcp.get_tool(context.message.name)
                user_roles = self._get_user_roles()

                if not self._has_access_to_tool(getattr(tool, "tags", []), user_roles):
                    raise ToolError("Access denied. You do not have permission to execute this tool.")
                    
                if not tool.enabled:
                    raise ToolError("Tool is currently disabled")
                    
            except Exception:
                # Tool not found or other error - let execution continue
                # and handle the error naturally
                pass
        
        return await call_next(context)
