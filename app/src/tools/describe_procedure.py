from mcp.server.fastmcp import FastMCP
from src.repositories.procedure_repository import get_procedure_details

def register(mcp: FastMCP):

    @mcp.tool()
    def describe_procedure(procedure_name: str):
        
        return get_procedure_details(procedure_name)