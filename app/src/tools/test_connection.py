from mcp.server.fastmcp import FastMCP
from src.repositories.procedure_repository import get_test_connection

def register(mcp: FastMCP):

    @mcp.tool()
    # Prueba de conexion
    def test_connection():
        row = get_test_connection()
        return row