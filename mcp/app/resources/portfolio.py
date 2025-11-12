"""
Portfolio data resources exposed via MCP.
"""

import io
from fastmcp.server.dependencies import get_access_token
import httpx
import pandas as pd

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError
from app.config.settings import settings


class PortfolioResourceProvider:
    """
    Provider for portfolio data resources.

    Exposes portfolio CSV data as MCP resources that can be
    inspected by LLM clients.
    """

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.register_resources()

    def register_resources(self):
        """Register portfolio resources."""
        self.mcp.resource(
            "resource://portfolio/csv/raw",
            name="Raw Portfolio Data",
            description="Complete portfolio positions data in CSV format",
            mime_type="text/csv",
        )(self.get_portfolio_csv_raw)

        self.mcp.resource(
            "resource://portfolio/csv/by-pm/{pm}",
            name="Portfolio Data by PM",
            description="Portfolio positions filtered by Portfolio Manager",
            mime_type="text/csv",
        )(self.get_portfolio_by_pm)

        self.mcp.resource(
            "resource://portfolio/csv/summary",
            name="Portfolio Summary",
            description="High-level summary of portfolio data",
            mime_type="text/markdown",
        )(self.get_portfolio_summary)

    async def _fetch_portfolio_data(self) -> str:
        """
        Fetch portfolio CSV data from the API.

        Args:
            access_token: Optional bearer token for authentication

        Returns:
            CSV string data
        """
        access_token = get_access_token()

        if access_token is None:
            raise ValueError("No access token found")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.portfolio_api_url}/portfolio/csv",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.text

    async def get_portfolio_csv_raw(self) -> str:
        """
        Get the raw portfolio CSV data.

        This resource provides access to the complete portfolio CSV
        with all columns and rows.

        Returns:
            CSV string data
        """
        try:
            csv_data = await self._fetch_portfolio_data()
            return csv_data
        except Exception as e:
            raise ResourceError(f"Error loading portfolio data: {str(e)}")

    async def get_portfolio_by_pm(self, pm: str) -> str:
        """
        Get filtered portfolio data for a specific PM.

        Args:
            pm: Portfolio Manager name to filter by

        Returns:
            CSV string with filtered portfolio data for the PM
        """
        try:
            csv_data = await self._fetch_portfolio_data()
            df = pd.read_csv(io.StringIO(csv_data))  # pyright: ignore[reportUnknownMemberType]

            # Filter by PM
            if "PM" not in df.columns:
                raise ResourceError("PM column not found in portfolio data")

            pm_df = df[df["PM"] == pm]

            if pm_df.empty:
                # Return empty CSV with headers for consistency
                output = io.StringIO()
                pd.DataFrame(columns=df.columns).to_csv(output, index=False)
                return output.getvalue()

            # Convert back to CSV
            output = io.StringIO()
            pm_df.to_csv(output, index=False)
            return output.getvalue()

        except ResourceError:
            raise
        except Exception as e:
            raise ResourceError(f"Error loading portfolio data: {str(e)}")

    async def get_portfolio_summary(self) -> str:
        """
        Get a summary of the portfolio data.

        Provides high-level statistics about the portfolio:
        - Number of positions
        - List of PMs
        - Total GMV, NPV
        - Asset class breakdown

        Returns:
            Markdown string containing portfolio summary
        """
        try:
            csv_data = await self._fetch_portfolio_data()
            df = pd.read_csv(io.StringIO(csv_data))  # pyright: ignore[reportUnknownMemberType]

            summary_lines: list[str] = []
            summary_lines.append("# Portfolio Summary\n")

            # Basic statistics
            summary_lines.append(f"**Total Positions:** {len(df)}")

            if "PM" in df.columns:
                unique_pms = df["PM"].dropna().unique()
                summary_lines.append(f"**Number of PMs:** {len(unique_pms)}")
                summary_lines.append(
                    f"**PM List:** {', '.join(sorted(unique_pms[:10]))}"
                )
                if len(unique_pms) > 10:
                    summary_lines.append(f"  ... and {len(unique_pms) - 10} more")

            summary_lines.append("")

            # Financial metrics
            summary_lines.append("## Financial Metrics")

            metrics_to_sum = [
                ("GMVUSD", "Total GMV"),
                ("NPVUSD", "Total NPV"),
                ("DayPL", "Total Day P&L"),
                ("YTDPnL", "Total YTD P&L"),
            ]

            for col, label in metrics_to_sum:
                if col in df.columns:
                    value = pd.to_numeric(df[col], errors="coerce").sum()  # pyright: ignore[reportUnknownMemberType, reportAny]
                    summary_lines.append(f"- **{label}:** ${value:,.2f}")

            summary_lines.append("")

            # Asset class breakdown
            if "InstClass" in df.columns:
                summary_lines.append("## Asset Class Breakdown")
                asset_counts = df["InstClass"].value_counts()
                for asset_class, count in asset_counts.head(10).items():
                    summary_lines.append(f"- {asset_class}: {count} positions")

            # Underlying instruments
            if "UnderlyingInstrument" in df.columns:
                summary_lines.append("\n## Top Underlying Instruments")
                underlying_counts = df["UnderlyingInstrument"].value_counts()
                for underlying, count in underlying_counts.head(10).items():
                    if underlying and str(underlying).strip():
                        summary_lines.append(f"- {underlying}: {count} positions")

            return "\n".join(summary_lines)

        except Exception as e:
            raise ResourceError(f"Error generating portfolio summary: {str(e)}")
