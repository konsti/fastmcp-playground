"""
Base classes for tool providers.
"""

from abc import ABC, abstractmethod
from fastmcp import FastMCP


class BaseToolProvider(ABC):
    """Base class for tool providers."""
    
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.register_tools()
    
    @abstractmethod
    def register_tools(self):
        """
        Register this provider's tools with the MCP server.
        
        Subclasses should implement this method to register their tools
        using self.mcp.tool(self.method_name).
        """
        pass
