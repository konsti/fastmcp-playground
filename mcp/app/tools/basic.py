"""
Basic utility tools.

This provider demonstrates a simple tool provider pattern.
"""

from fastmcp import FastMCP
from app.tools.base import BaseToolProvider


class BasicToolProvider(BaseToolProvider):
    """Basic tool provider."""

    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        self.mcp.tool(self.greet)
        self.mcp.tool(self.echo)
        self.mcp.tool(self.add_numbers)
    
    def greet(self, name: str) -> str:
        """
        Greet a user by name.
        
        Args:
            name: The name of the person to greet
            
        Returns:
            A greeting message
        """
        return f"Hello, {name}!"
    
    def echo(self, message: str) -> str:
        """
        Echo back a message.
        
        Args:
            message: The message to echo
            
        Returns:
            The same message
        """
        return message
    
    def add_numbers(self, a: float, b: float) -> float:
        """
        Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of the two numbers
        """
        return a + b
