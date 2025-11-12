"""
Portfolio-related tools.

This module provides tools for accessing portfolio insights and data.
"""

from typing import Any, override
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from app.tools.base import BaseToolProvider
from app.icons import notebook_tabs


class PortfolioToolProvider(BaseToolProvider):
    """
    Provider for portfolio-related tools.
    """

    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)

    @override
    def register_tools(self):
        self.mcp.tool(
            name="portfolio_insights",
            title="Portfolio Insights",
            description="Get insights about the user's portfolio.",
            tags={"role:portfolio_access"},
            icons=[notebook_tabs],
            annotations=ToolAnnotations(
                title="Portfolio Insights",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=True
            ),
            meta={
                "unique.app/system-prompt": "Use this tool to get insights about the user's portfolio.",
            },
        )(self.portfolio_insights)

    def portfolio_insights(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
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
