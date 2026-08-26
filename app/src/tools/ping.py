from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def ping() -> str:
        """Verifica que el servidor MCP esté funcionando."""
        return "MCP funcionando"