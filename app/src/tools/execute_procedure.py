from mcp.server.fastmcp import FastMCP
from src.repositories.procedure_repository import execute_procedure


def register(mcp: FastMCP):

    @mcp.tool()
    def execute_procedures(
        procedure_name: str,
        procedure_parameters: dict | None = None):
        
        """
        Ejecuta un procedimiento almacenado registrado en el catálogo MCP.

        Parámetros:
        - procedure_name: Nombre del procedimiento almacenado.
        - procedure_parameters: Diccionario con los parámetros requeridos por el procedimiento.

        El procedimiento debe estar registrado y habilitado en el catálogo MCP.
        """
        print(f"Ejecutando procedimiento: {procedure_name} con parámetros: {procedure_parameters}")
        return execute_procedure(
            procedure_name,
            procedure_parameters
        )