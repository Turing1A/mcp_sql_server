from mcp.server.fastmcp import FastMCP
from src.repositories.procedure_repository import get_procedures


def register(mcp: FastMCP):

    @mcp.tool()
    def list_procedures():
        """
        Retorna la lista de procedimientos almacenados registrados y habilitados
        en el catálogo MCP.
        """
        return get_procedures()