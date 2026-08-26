import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=172.27.83.199,1443;"
        "DATABASE=master;"
        "UID=test;"
        "PWD=test**2026;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=5;"
    )

    print("Conectado correctamente")
    conn.close()

except Exception as e:
    print(repr(e))