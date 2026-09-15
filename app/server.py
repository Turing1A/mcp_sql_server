from mcp.server.fastmcp import FastMCP
from src.tools.ping import register as register_ping
from src.tools.test_connection import register as register_test_connection
from src.tools.list_procedures import register as register_list_procedures
from src.tools.describe_procedure import register as register_describe_procedure
from src.tools.execute_procedure import register as register_execute_procedure
#from src.tools.authentication import register as register_authentication
import os
import pyodbc

from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "SQL Server MCP",
    host="0.0.0.0",
    port=8000,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
        allowed_hosts=["*"]
    )
)


def main():

    # Registrar herramientas 
    register_ping(mcp)
    register_test_connection(mcp)
    register_list_procedures(mcp)
    register_describe_procedure(mcp)
    register_execute_procedure(mcp)
    ##register_authentication(mcp)
    
    # Iniciar servidor
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()