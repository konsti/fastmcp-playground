"""
Authentication-related demo tools.
"""

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.dependencies import get_access_token
from app.tools.base import BaseToolProvider


class AuthToolProvider(BaseToolProvider):
    """
    Provider for authentication-related tools.
    
    This demonstrates how a class can share common authentication
    logic across multiple tools.
    """
    
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        self.mcp.tool(tags=["role:all"])(self.get_user_info)
        self.mcp.tool(tags=["role:all"])(self.check_authentication)
        self.mcp.tool(tags=["role:all"])(self.get_token_claims)
    
    def _get_token(self) -> AccessToken | None:
        """
        Internal helper to get the current Keycloak access token.
        
        Returns:
            The current Keycloak access token or None if not authenticated
        """
        return get_access_token()
    
    def get_user_info(self) -> dict:
        """
        Get information about the authenticated user.
        
        Returns:
            Dictionary containing user authentication information including:
            - authenticated: Whether the user is authenticated
            - client_id: The OAuth client ID (if authenticated)
            - scopes: List of granted scopes (if authenticated)
            - expires_at: Token expiration time (if authenticated)
            - token_claims: JWT claims (if authenticated)
        """
        token = self._get_token()
        
        if token is None:
            return {"authenticated": False}
        
        return {
            "authenticated": True,
            "client_id": token.client_id,
            "scopes": token.scopes,
            "expires_at": token.expires_at,
            "token_claims": token.claims,
        }
    
    def check_authentication(self) -> dict:
        """
        Check if the current request is authenticated.
        
        Returns:
            Dictionary with authentication status
        """
        token = self._get_token()
        return {
            "authenticated": token is not None,
            "message": "User is authenticated" if token else "User is not authenticated"
        }
    
    def get_token_claims(self) -> dict:
        """
        Get the JWT claims from the current access token.
        
        Returns:
            Dictionary containing JWT claims or error message
        """
        token = self._get_token()
        
        if token is None:
            return {"error": "Not authenticated"}
        
        return token.claims or {}
