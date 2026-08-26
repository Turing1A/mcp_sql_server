import os
import pyodbc
"""
Recibe: null
devuelve: str
"""
def get_connection():
    """Prueba la conexión al SQL Server."""
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    user = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    
  
    
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
        "Connection Timeout=5;"
        )
    
    session_parameter ="""
    SET ARITHABORT ON;
    SET ANSI_WARNINGS ON;
    SET QUOTED_IDENTIFIER ON;
    SET ANSI_NULLS ON;
    SET CONCAT_NULL_YIELDS_NULL ON;
    SET ANSI_PADDING ON;
    SET NOCOUNT ON;
    """

    conn = pyodbc.connect(connection_string, timeout=5)

    cursor = conn.cursor()
    cursor.execute(session_parameter)
    cursor.close()

    return conn