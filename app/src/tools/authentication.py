from mcp.server.fastmcp import FastMCP
from src.repositories.procedure_repository import aut_user


def register(mcp: FastMCP):
    @mcp.tool()
    def auth_user(userID: int):
        """
        Autentica un usuario en la base de datos.
        """

        return aut_user(userID)