"""
Sandbox tool for executing Python code in an isolated environment.

This module provides tools for securely running Python code using llm-sandbox.
"""

from typing import Any, override
from fastmcp import FastMCP
from llm_sandbox import SandboxBackend  # pyright: ignore[reportMissingTypeStubs]
from mcp.types import ToolAnnotations
from app.tools.base import BaseToolProvider
from app.icons import code


class SandboxToolProvider(BaseToolProvider):
    """
    Provider for code execution sandbox tools.
    """

    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)

    @override
    def register_tools(self):
        self.mcp.tool(
            name="run_python_code",
            title="Run Python Code",
            description="Run Python code in a secure sandbox environment.",
            tags={"role:all"},
            icons=[code],
            annotations=ToolAnnotations(
                title="Run Python Code",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=True,
            ),
            meta={
                "unique.app/system-prompt": "Use this tool to run Python code in a secure sandbox environment.",
            },
        )(self.run_python_code)

    def run_python_code(self, code: str, timeout: int = 30) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        """
        Execute Python code in a secure sandbox environment.

        Args:
            code: The Python code to execute
            timeout: Maximum execution time in seconds (default: 30)

        Returns:
            A dictionary containing:
            - stdout: Standard output from the code execution
            - stderr: Standard error from the code execution
            - exit_code: Exit code of the execution (0 for success)
            - success: Boolean indicating if execution was successful
        """
        try:
            from llm_sandbox import SandboxSession  # pyright: ignore[reportMissingTypeStubs]

            with SandboxSession(
                lang="python",
                backend=SandboxBackend.DOCKER,
            ) as session:
                result = session.run(code, timeout=timeout)  # pyright: ignore[reportUnknownMemberType]

                return {
                    "stdout": result.stdout or "",
                    "stderr": result.stderr or "",
                    "exit_code": result.exit_code,
                    "success": result.exit_code == 0,
                }

        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error executing code: {str(e)}",
                "exit_code": 1,
                "success": False,
            }
