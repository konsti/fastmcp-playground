"""
Portfolio-related tools.

This module provides tools for accessing portfolio insights and data.
"""

from fastmcp import FastMCP
from app.tools.base import BaseToolProvider


class PortfolioToolProvider(BaseToolProvider):
    """
    Provider for portfolio-related tools.
    """
    
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        self.mcp.tool(tags=["role:portfolio_access"])(self.portfolio_insights)
    
    def portfolio_insights(self) -> dict:
        """
        Get insights about the user's portfolio.
        """
        # In a real implementation, this would fetch actual portfolio data
        # For now, return sample insights
        return {
            "total_value": 125000.00,
            "currency": "USD",
            "asset_count": 15,
            "performance": {
                "daily_change": 1.2,
                "weekly_change": 3.5,
                "monthly_change": 8.7,
                "yearly_change": 22.3,
            },
            "risk_level": "moderate",
            "top_holdings": [
                {"symbol": "AAPL", "value": 25000.00, "percentage": 20.0},
                {"symbol": "GOOGL", "value": 18750.00, "percentage": 15.0},
                {"symbol": "MSFT", "value": 15625.00, "percentage": 12.5},
            ],
            "asset_allocation": {
                "stocks": 70.0,
                "bonds": 20.0,
                "cash": 10.0,
            },
        }


