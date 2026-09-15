from src.connections.database import get_connection
import time


"""
recibe: dict
devuelve: dict[list(tuple)]
"""


def get_sql_version() -> dict:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")

        return cursor.fetchone()[0]

    finally:
        conn.close()


def execute_query(query: str, parameters: tuple = ()):
    inicio = time.perf_counter()
    conn = get_connection()
    fin = time.perf_counter()

    try:
        # ---------------------------------------------------------
        # CREAR CURSOR
        # ---------------------------------------------------------
     
        cursor = conn.cursor()
     

        # ---------------------------------------------------------
        # EJECUTAR CONSULTA
        # ---------------------------------------------------------
      
        cursor.execute(query, parameters)
     
        # ---------------------------------------------------------
        # METADATA
        # ---------------------------------------------------------
        metadata = cursor.description

        # ---------------------------------------------------------
        # FETCHALL
        # ---------------------------------------------------------
      
        rows = cursor.fetchall()
      

        # ---------------------------------------------------------
        # SIN FILAS
        # ---------------------------------------------------------
        if not rows:
            return {
                "has_data": False,
                "metadata": metadata,
                "rows": [],
                "message": (
                    "No se encontraron datos para "
                    "los parámetros enviados."
                )
            }

        # ---------------------------------------------------------
        # FILA CON TODOS LOS VALORES NULL
        # ---------------------------------------------------------
        if all(value is None for value in rows[0]):
            return {
                "has_data": False,
                "metadata": metadata,
                "rows": [],
                "message": (
                    "No se encontraron datos para "
                    "los parámetros enviados."
                )
            }

        # ---------------------------------------------------------
        # CONSULTA CON DATOS
        # ---------------------------------------------------------
        resultado = {
            "has_data": True,
            "metadata": metadata,
            "rows": rows,
            "message": "Datos encontrados correctamente."
        }

        return resultado

    finally:
        conn.close()