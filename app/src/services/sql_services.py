from src.connections.database import get_connection
import time


print("🔥🔥🔥 CARGANDO sql_services.py 🔥🔥🔥")


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
    print("🔥🔥🔥 ENTRE A execute_query 🔥🔥🔥")

    print("\n" + "=" * 80)
    print("[SQL_SERVICE] execute_query() - INICIO")
    print("=" * 80)

    print("[SQL_SERVICE] QUERY:")
    print(query)

    print(f"[SQL_SERVICE] PARAMETERS: {parameters}")

    print("[SQL_SERVICE] Obteniendo conexión...")

    inicio = time.perf_counter()

    conn = get_connection()

    fin = time.perf_counter()

    print(
        f"[SQL_SERVICE] get_connection() terminó en "
        f"{fin - inicio:.2f} segundos"
    )

    try:

        # ---------------------------------------------------------
        # CREAR CURSOR
        # ---------------------------------------------------------

        print("[SQL_SERVICE] Creando cursor...")

        inicio = time.perf_counter()

        cursor = conn.cursor()

        fin = time.perf_counter()

        print(
            f"[SQL_SERVICE] conn.cursor() terminó en "
            f"{fin - inicio:.2f} segundos"
        )

        # ---------------------------------------------------------
        # EJECUTAR CONSULTA
        # ---------------------------------------------------------

        print("[SQL_SERVICE] Ejecutando cursor.execute()...")

        inicio = time.perf_counter()

        cursor.execute(query, parameters)

        fin = time.perf_counter()

        print(
            f"[SQL_SERVICE] cursor.execute() TERMINÓ en "
            f"{fin - inicio:.2f} segundos"
        )

        # ---------------------------------------------------------
        # METADATA
        # ---------------------------------------------------------

        print("[SQL_SERVICE] Obteniendo metadata...")

        metadata = cursor.description

        print(
            f"[SQL_SERVICE] Metadata obtenida. "
            f"Columnas: {len(metadata) if metadata else 0}"
        )

        # ---------------------------------------------------------
        # FETCHALL
        # ---------------------------------------------------------

        print("[SQL_SERVICE] Ejecutando cursor.fetchall()...")

        inicio = time.perf_counter()

        rows = cursor.fetchall()

        fin = time.perf_counter()

        print(
            f"[SQL_SERVICE] cursor.fetchall() TERMINÓ en "
            f"{fin - inicio:.2f} segundos"
        )

        print(
            f"[SQL_SERVICE] Cantidad de filas obtenidas: "
            f"{len(rows)}"
        )

        # ---------------------------------------------------------
        # SIN FILAS
        # ---------------------------------------------------------

        if not rows:

            print(
                "[SQL_SERVICE] La consulta no devolvió filas."
            )

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

        print(
            "[SQL_SERVICE] Validando si la primera fila "
            "contiene únicamente valores NULL..."
        )

        if all(value is None for value in rows[0]):

            print(
                "[SQL_SERVICE] CONSULTA SIN DATOS - "
                "TODOS LOS VALORES SON NULL"
            )

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

        print("[SQL_SERVICE] Consulta contiene datos.")

        print("[SQL_SERVICE] Preparando resultado...")

        resultado = {
            "has_data": True,
            "metadata": metadata,
            "rows": rows,
            "message": "Datos encontrados correctamente."
        }

        print("[SQL_SERVICE] Resultado preparado correctamente.")

        return resultado

    finally:

        print("[SQL_SERVICE] Cerrando conexión...")

        conn.close()

        print("[SQL_SERVICE] Conexión cerrada.")

        print("[SQL_SERVICE] execute_query() - FIN")

        print("=" * 80)