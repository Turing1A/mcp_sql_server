from time import perf_counter

from src.services.sql_services import execute_query
from src.utils.serializer import serialize_rows


# -----------------------------------------------------------------------
# EXECUTE AND SERIALIZE
# -----------------------------------------------------------------------
from src.services.sql_services import execute_query
from src.utils.serializer import serialize_rows


def execute_and_serialize(sql: str, parameters: tuple = ()):
    """
    Ejecuta una consulta SQL y serializa el resultado.
    """

    print("\n" + "=" * 80)
    print("[REPOSITORY] execute_and_serialize() - INICIO")
    print("=" * 80)

    print("[REPOSITORY] SQL:")
    print(sql)

    print(f"[REPOSITORY] PARAMETERS: {parameters}")

    # ---------------------------------------------------------
    # DIAGNÓSTICO DE execute_query
    # ---------------------------------------------------------

    print("[REPOSITORY] ANTES de execute_query()")

    print(
        "[REPOSITORY] execute_query OBJECT:",
        execute_query
    )

    print(
        "[REPOSITORY] execute_query MODULE:",
        execute_query.__module__
    )

    print(
        "[REPOSITORY] execute_query NAME:",
        execute_query.__name__
    )

    # ---------------------------------------------------------
    # EJECUTAR CONSULTA
    # ---------------------------------------------------------

    resultado = execute_query(
        sql,
        parameters
    )

    print("[REPOSITORY] DESPUÉS de execute_query()")

    # ---------------------------------------------------------
    # VALIDAR RESULTADO
    # ---------------------------------------------------------

    print(
        "[REPOSITORY] has_data:",
        resultado.get("has_data")
    )

    print(
        "[REPOSITORY] cantidad de columnas:",
        len(resultado.get("metadata", []))
    )

    print(
        "[REPOSITORY] cantidad de filas:",
        len(resultado.get("rows", []))
    )

    # ---------------------------------------------------------
    # SERIALIZAR
    # ---------------------------------------------------------

    print("[REPOSITORY] ANTES de serialize_rows()")

    resultado_serializado = serialize_rows(resultado)

    print("[REPOSITORY] DESPUÉS de serialize_rows()")

    print(
        "[REPOSITORY] Resultado serializado - has_data:",
        resultado_serializado.get("has_data")
    )

    print(
        "[REPOSITORY] Resultado serializado - cantidad de registros:",
        len(resultado_serializado.get("data", []))
    )

    print("[REPOSITORY] execute_and_serialize() - FIN")
    print("=" * 80)

    return resultado_serializado


# -----------------------------------------------------------------------
# GET PROCEDURES
# -----------------------------------------------------------------------
def get_procedures():

    inicio = perf_counter()

    print("\n" + "#" * 80, flush=True)
    print(
        "[REPOSITORY] get_procedures() - INICIO",
        flush=True
    )
    print("#" * 80, flush=True)

    sql = """
        EXEC bi.mcp_listar_sp
    """

    print(
        "[REPOSITORY] ANTES de execute_query()",
        flush=True
    )

    resultado = execute_query(sql)

    print(
        "[REPOSITORY] DESPUÉS de execute_query()",
        flush=True
    )

    resultado_serializado = serialize_rows(resultado)

    print(
        "[REPOSITORY] DESPUÉS de serialize_rows()",
        flush=True
    )

    tiempo = perf_counter() - inicio

    print(
        f"[REPOSITORY] Tiempo total: "
        f"{tiempo:.3f} segundos",
        flush=True
    )

    print(
        "[REPOSITORY] get_procedures() - FIN",
        flush=True
    )

    return resultado_serializado


# -----------------------------------------------------------------------
# TEST CONNECTION
# -----------------------------------------------------------------------
def get_test_connection():

    inicio = perf_counter()

    print("\n" + "#" * 80, flush=True)
    print(
        "[REPOSITORY] get_test_connection() - INICIO",
        flush=True
    )
    print("#" * 80, flush=True)

    sql = """
        SELECT DB_NAME()
    """

    print(
        "[REPOSITORY] ANTES de execute_query()",
        flush=True
    )

    resultado = execute_query(sql)

    print(
        "[REPOSITORY] DESPUÉS de execute_query()",
        flush=True
    )

    resultado_serializado = serialize_rows(resultado)

    print(
        "[REPOSITORY] Resultado serializado:",
        flush=True
    )

    print(
        resultado_serializado,
        flush=True
    )

    tiempo = perf_counter() - inicio

    print(
        f"[REPOSITORY] Tiempo total: "
        f"{tiempo:.3f} segundos",
        flush=True
    )

    print(
        "[REPOSITORY] get_test_connection() - FIN",
        flush=True
    )

    return resultado_serializado


# -----------------------------------------------------------------------
# GET PROCEDURE DETAILS
# -----------------------------------------------------------------------
def get_procedure_details(
    procedure_name: str
):

    inicio = perf_counter()

    print("\n" + "#" * 80, flush=True)
    print(
        "[REPOSITORY] get_procedure_details() - INICIO",
        flush=True
    )
    print("#" * 80, flush=True)

    print(
        f"[REPOSITORY] procedure_name: "
        f"{procedure_name}",
        flush=True
    )

    sql = """
        EXEC bi.mcp_descripcion_sp ?
    """

    print(
        "[REPOSITORY] SQL:",
        flush=True
    )

    print(
        sql.strip(),
        flush=True
    )

    print(
        "[REPOSITORY] ANTES de execute_query()",
        flush=True
    )

    resultado = execute_query(
        sql,
        (procedure_name,)
    )

    print(
        "[REPOSITORY] DESPUÉS de execute_query()",
        flush=True
    )

    print(
        f"[REPOSITORY] has_data: "
        f"{resultado['has_data']}",
        flush=True
    )

    print(
        f"[REPOSITORY] columnas: "
        f"{len(resultado['metadata'])}",
        flush=True
    )

    print(
        f"[REPOSITORY] filas: "
        f"{len(resultado['rows'])}",
        flush=True
    )

    print(
        "[REPOSITORY] ANTES de serialize_rows()",
        flush=True
    )

    resultado_serializado = serialize_rows(resultado)

    print(
        "[REPOSITORY] DESPUÉS de serialize_rows()",
        flush=True
    )

    print(
        f"[REPOSITORY] Cantidad de registros serializados: "
        f"{len(resultado_serializado['data'])}",
        flush=True
    )

    if not resultado_serializado["has_data"]:

        print(
            "[REPOSITORY] ERROR: No existe información para "
            f"'{procedure_name}'",
            flush=True
        )

        raise Exception(
            f"No existe información para el procedimiento "
            f"'{procedure_name}'."
        )

    rows = resultado_serializado["data"]

    print(
        f"[REPOSITORY] Cantidad de filas obtenidas: "
        f"{len(rows)}",
        flush=True
    )

    # ---------------------------------------------------------
    # Construir definición
    # ---------------------------------------------------------

    print(
        "[REPOSITORY] Construyendo definición del procedimiento",
        flush=True
    )

    procedure = {
        "schema": rows[0]["schema_name"],
        "proc_almacenado": rows[0]["proc_almacenado"],
        "descripcion": rows[0]["descripcion_parametro"],
        "use_cases": rows[0]["use_cases"],
        "parameters": []
    }

    print(
        f"[REPOSITORY] Schema: "
        f"{procedure['schema']}",
        flush=True
    )

    print(
        f"[REPOSITORY] Procedimiento: "
        f"{procedure['proc_almacenado']}",
        flush=True
    )

    # ---------------------------------------------------------
    # Construir parámetros
    # ---------------------------------------------------------

    for row in rows:

        print(
            "[REPOSITORY] Procesando parámetro: "
            f"{row['parameter_name']}",
            flush=True
        )

        procedure["parameters"].append(
            {
                "name": row["parameter_name"],
                "type": row["parameter_type"],
                "required": row["required"],
                "example": row["example"],
                "orden": row["orden"]
            }
        )

    print(
        "[REPOSITORY] TERMINÓ FOR DE PARAMETROS",
        flush=True
    )

    print(
        "[REPOSITORY] Cantidad de parámetros: "
        f"{len(procedure['parameters'])}",
        flush=True
    )

    tiempo = perf_counter() - inicio

    print(
        f"[REPOSITORY] Tiempo get_procedure_details(): "
        f"{tiempo:.3f} segundos",
        flush=True
    )

    print(
        "[REPOSITORY] get_procedure_details() - FIN",
        flush=True
    )

    return procedure


# -----------------------------------------------------------------------
# EXECUTE PROCEDURE
# -----------------------------------------------------------------------
def execute_procedure(
    procedure_name: str,
    parametros_enviados: dict | None = None
):

    inicio_total = perf_counter()

    print("\n" + "=" * 100, flush=True)
    print(
        "[REPOSITORY] execute_procedure() - INICIO",
        flush=True
    )
    print("=" * 100, flush=True)

    print(
        f"[REPOSITORY] PROCEDURE: "
        f"{procedure_name}",
        flush=True
    )

    print(
        f"[REPOSITORY] PARAMETROS ENVIADOS: "
        f"{parametros_enviados}",
        flush=True
    )

    # ---------------------------------------------------------
    # Normalizar None
    # ---------------------------------------------------------

    if parametros_enviados is None:

        print(
            "[REPOSITORY] parametros_enviados es None",
            flush=True
        )

        parametros_enviados = {}

    print(
        "[REPOSITORY] parametros_enviados listo",
        flush=True
    )

    sql = """
        SELECT bi.CONSULTAR_PROCEDIMIENTO_EXISTENTE(?)
    """

    try:

        # =====================================================
        # PASO 1
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 1 - "
            "Validar existencia del procedimiento",
            flush=True
        )

        resultado = execute_and_serialize(
            sql,
            (procedure_name,)
        )

        print(
            "[REPOSITORY] PASO 1 TERMINADO",
            flush=True
        )

        if not resultado["has_data"]:

            raise Exception(
                f"El procedimiento '{procedure_name}' "
                f"no existe o no está habilitado."
            )

        print(
            "[REPOSITORY] Procedimiento válido.",
            flush=True
        )

        # =====================================================
        # PASO 2
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 2 - "
            "Obtener definición del procedimiento",
            flush=True
        )

        inicio_paso_2 = perf_counter()

        procedure_definition = get_procedure_details(
            procedure_name
        )

        print(
            "[REPOSITORY] get_procedure_details() TERMINÓ",
            flush=True
        )

        print(
            f"[REPOSITORY] Schema obtenido: "
            f"{procedure_definition['schema']}",
            flush=True
        )

        print(
            f"[REPOSITORY] Procedimiento obtenido: "
            f"{procedure_definition['proc_almacenado']}",
            flush=True
        )

        parametros_catalogo = (
            procedure_definition["parameters"]
        )

        schema = procedure_definition["schema"]

        print(
            "[REPOSITORY] Cantidad de parámetros del catálogo: "
            f"{len(parametros_catalogo)}",
            flush=True
        )

        print(
            f"[REPOSITORY] Tiempo PASO 2: "
            f"{perf_counter() - inicio_paso_2:.3f} segundos",
            flush=True
        )

        # =====================================================
        # PASO 3
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 3 - "
            "Verificar si el procedimiento tiene parámetros",
            flush=True
        )

        if not parametros_catalogo:

            print(
                "[REPOSITORY] Procedimiento SIN parámetros",
                flush=True
            )

            sql = f"""
                EXEC {schema}.{procedure_name}
            """

            resultado = execute_and_serialize(sql)

            print(
                "[REPOSITORY] execute_procedure() - FIN",
                flush=True
            )

            return resultado

        print(
            "[REPOSITORY] Procedimiento CON parámetros",
            flush=True
        )

        # =====================================================
        # PASO 4
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 4 - "
            "Validar parámetros",
            flush=True
        )

        print(
            "[REPOSITORY] ANTES de llamar validar_parametros()",
            flush=True
        )

        inicio_validacion = perf_counter()

        resultado_validacion = validar_parametros(
            parametros_catalogo,
            parametros_enviados
        )

        print(
            "[REPOSITORY] DESPUÉS de llamar validar_parametros()",
            flush=True
        )

        print(
            f"[REPOSITORY] Tipo resultado_validacion: "
            f"{type(resultado_validacion)}",
            flush=True
        )

        print(
            f"[REPOSITORY] Resultado validacion: "
            f"{resultado_validacion}",
            flush=True
        )

        print(
            f"[REPOSITORY] Tiempo validar_parametros(): "
            f"{perf_counter() - inicio_validacion:.3f} segundos",
            flush=True
        )

        print(
            "[REPOSITORY] ANTES de desempaquetar resultado_validacion",
            flush=True
        )

        parameter_placeholders, parameter_values = (
            resultado_validacion
        )

        print(
            "[REPOSITORY] DESPUÉS de desempaquetar",
            flush=True
        )

        print(
            "[REPOSITORY] PASO 4 TERMINADO",
            flush=True
        )

        print(
            "[REPOSITORY] PARAMETER PLACEHOLDERS: "
            f"{parameter_placeholders}",
            flush=True
        )

        print(
            "[REPOSITORY] PARAMETER VALUES: "
            f"{parameter_values}",
            flush=True
        )

        # =====================================================
        # PASO 5
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 5 - "
            "Construir ejecución del procedimiento",
            flush=True
        )

        print(
            "[REPOSITORY] ANTES de construir SQL",
            flush=True
        )

        sql = f"""
            EXEC {schema}.{procedure_name}
            {', '.join(parameter_placeholders)}
        """

        print(
            "[REPOSITORY] DESPUÉS de construir SQL",
            flush=True
        )

        print(
            "[REPOSITORY] SQL FINAL:",
            flush=True
        )

        print(
            sql.strip(),
            flush=True
        )

        # =====================================================
        # PASO 6
        # =====================================================

        print(
            "\n[REPOSITORY] PASO 6 - "
            "EJECUTANDO PROCEDIMIENTO EN SQL SERVER",
            flush=True
        )

        print(
            "[REPOSITORY] Parameters: "
            f"{tuple(parameter_values)}",
            flush=True
        )

        print(
            "[REPOSITORY] ANTES de execute_and_serialize() "
            "DEL PROCEDIMIENTO",
            flush=True
        )

        inicio_sp = perf_counter()

        resultado = execute_and_serialize(
            sql,
            tuple(parameter_values)
        )

        tiempo_sp = perf_counter() - inicio_sp

        print(
            "[REPOSITORY] DESPUÉS de execute_and_serialize() "
            "DEL PROCEDIMIENTO",
            flush=True
        )

        print(
            f"[REPOSITORY] TIEMPO EJECUCIÓN SP: "
            f"{tiempo_sp:.3f} segundos",
            flush=True
        )

        print(
            "\n[REPOSITORY] PASO 6 TERMINADO",
            flush=True
        )

        print(
            "[REPOSITORY] Resultado del procedimiento:",
            flush=True
        )

        print(
            resultado,
            flush=True
        )

        tiempo_total = perf_counter() - inicio_total

        print(
            f"\n[REPOSITORY] TIEMPO TOTAL: "
            f"{tiempo_total:.3f} segundos",
            flush=True
        )

        print(
            "[REPOSITORY] execute_procedure() - FIN",
            flush=True
        )

        return resultado

    except Exception as e:

        print(
            "\n[REPOSITORY] ERROR EN execute_procedure()",
            flush=True
        )

        print(
            f"[REPOSITORY] Tipo de error: "
            f"{type(e).__name__}",
            flush=True
        )

        print(
            f"[REPOSITORY] Mensaje: {e}",
            flush=True
        )

        raise Exception(
            f"Error ejecutando el procedimiento "
            f"'{procedure_name}': {e}"
        ) from e


# -----------------------------------------------------------------------
# VALIDAR PARAMETROS
# -----------------------------------------------------------------------
def validar_parametros(
    parametros_catalogo: list,
    parametros_enviados: dict
) -> tuple[list[str], list]:

    print("\n" + "-" * 80, flush=True)
    print(
        "[VALIDACION] validar_parametros() - INICIO",
        flush=True
    )
    print("-" * 80, flush=True)

    print(
        "[VALIDACION] Parámetros enviados:",
        flush=True
    )

    print(
        parametros_enviados,
        flush=True
    )

    print(
        "[VALIDACION] Tipo parametros_enviados: "
        f"{type(parametros_enviados)}",
        flush=True
    )

    print(
        "[VALIDACION] Cantidad parámetros enviados: "
        f"{len(parametros_enviados)}",
        flush=True
    )

    print(
        "[VALIDACION] Cantidad parámetros catálogo: "
        f"{len(parametros_catalogo)}",
        flush=True
    )

    parameter_placeholders = []
    parameter_values = []
    parametros_validos = set()

    print(
        "[VALIDACION] Variables inicializadas correctamente",
        flush=True
    )

    # =========================================================
    # FOR CATÁLOGO
    # =========================================================

    print(
        "\n[VALIDACION] ANTES DEL FOR parametros_catalogo",
        flush=True
    )

    for indice, parametro in enumerate(
        parametros_catalogo,
        start=1
    ):

        print(
            "\n" + "." * 70,
            flush=True
        )

        print(
            f"[VALIDACION] INICIO ITERACION #{indice}",
            flush=True
        )

        print(
            f"[VALIDACION] Tipo parametro: "
            f"{type(parametro)}",
            flush=True
        )

        print(
            f"[VALIDACION] Contenido parametro: "
            f"{parametro}",
            flush=True
        )

        # -----------------------------------------------------
        # Obtener nombre
        # -----------------------------------------------------

        print(
            "[VALIDACION] ANTES de parametro['name']",
            flush=True
        )

        nombre_parametro_catalogo = parametro["name"]

        print(
            "[VALIDACION] parametro['name'] obtenido: "
            f"{nombre_parametro_catalogo}",
            flush=True
        )

        print(
            "[VALIDACION] ANTES de replace('@', '')",
            flush=True
        )

        nombre_parametro_catalogo = (
            nombre_parametro_catalogo.replace("@", "")
        )

        print(
            "[VALIDACION] Nombre normalizado: "
            f"{nombre_parametro_catalogo}",
            flush=True
        )

        # -----------------------------------------------------
        # Parámetros válidos
        # -----------------------------------------------------

        print(
            "[VALIDACION] ANTES de parametros_validos.add()",
            flush=True
        )

        parametros_validos.add(
            nombre_parametro_catalogo
        )

        print(
            "[VALIDACION] Parámetro agregado a "
            "parametros_validos",
            flush=True
        )

        # -----------------------------------------------------
        # Verificar si fue enviado
        # -----------------------------------------------------

        print(
            "[VALIDACION] Verificando si el parámetro está "
            "en parametros_enviados...",
            flush=True
        )

        print(
            "[VALIDACION] Buscando key: "
            f"{nombre_parametro_catalogo}",
            flush=True
        )

        if nombre_parametro_catalogo not in parametros_enviados:

            print(
                "[VALIDACION] Parámetro NO enviado: "
                f"{nombre_parametro_catalogo}",
                flush=True
            )

            print(
                "[VALIDACION] ANTES de consultar "
                "parametro['required']",
                flush=True
            )

            required = parametro["required"]

            print(
                "[VALIDACION] required: "
                f"{required}",
                flush=True
            )

            if required:

                print(
                    "[VALIDACION] ERROR: Parámetro obligatorio "
                    f"faltante: {nombre_parametro_catalogo}",
                    flush=True
                )

                raise Exception(
                    f"Falta el parámetro obligatorio "
                    f"'{nombre_parametro_catalogo}'."
                )

            print(
                "[VALIDACION] Parámetro opcional. "
                "Continuando...",
                flush=True
            )

            continue

        # -----------------------------------------------------
        # Parámetro enviado
        # -----------------------------------------------------

        print(
            "[VALIDACION] Parámetro ENVIADO: "
            f"{nombre_parametro_catalogo}",
            flush=True
        )

        # -----------------------------------------------------
        # Placeholder
        # -----------------------------------------------------

        print(
            "[VALIDACION] ANTES de construir placeholder",
            flush=True
        )

        placeholder = (
            f"@{nombre_parametro_catalogo}=?"
        )

        print(
            "[VALIDACION] Placeholder construido: "
            f"{placeholder}",
            flush=True
        )

        parameter_placeholders.append(
            placeholder
        )

        print(
            "[VALIDACION] Placeholder agregado",
            flush=True
        )

        # -----------------------------------------------------
        # Valor
        # -----------------------------------------------------

        print(
            "[VALIDACION] ANTES de obtener valor "
            "desde parametros_enviados",
            flush=True
        )

        valor = parametros_enviados[
            nombre_parametro_catalogo
        ]

        print(
            "[VALIDACION] Valor obtenido: "
            f"{valor}",
            flush=True
        )

        print(
            "[VALIDACION] Tipo del valor: "
            f"{type(valor)}",
            flush=True
        )

        parameter_values.append(valor)

        print(
            "[VALIDACION] Valor agregado a "
            "parameter_values",
            flush=True
        )

        print(
            f"[VALIDACION] FIN ITERACION #{indice}",
            flush=True
        )

    # =========================================================
    # FIN FOR
    # =========================================================

    print(
        "\n" + "." * 70,
        flush=True
    )

    print(
        "[VALIDACION] TERMINÓ FOR parametros_catalogo",
        flush=True
    )

    print(
        "[VALIDACION] Cantidad parametros_validos: "
        f"{len(parametros_validos)}",
        flush=True
    )

    print(
        "[VALIDACION] Parámetros válidos:",
        flush=True
    )

    print(
        parametros_validos,
        flush=True
    )

    print(
        "[VALIDACION] Placeholders:",
        flush=True
    )

    print(
        parameter_placeholders,
        flush=True
    )

    print(
        "[VALIDACION] Values:",
        flush=True
    )

    print(
        parameter_values,
        flush=True
    )

    # =========================================================
    # VALIDAR SOBRANTES
    # =========================================================

    print(
        "\n[VALIDACION] INICIO validación de parámetros "
        "enviados que no pertenecen al procedimiento",
        flush=True
    )

    print(
        "[VALIDACION] Cantidad parámetros enviados: "
        f"{len(parametros_enviados)}",
        flush=True
    )

    for indice, parametro_enviado in enumerate(
        parametros_enviados,
        start=1
    ):

        print(
            f"[VALIDACION] Revisando parámetro enviado "
            f"#{indice}: {parametro_enviado}",
            flush=True
        )

        print(
            "[VALIDACION] Verificando pertenencia en "
            "parametros_validos...",
            flush=True
        )

        if parametro_enviado not in parametros_validos:

            print(
                "[VALIDACION] ERROR: Parámetro no pertenece "
                "al procedimiento: "
                f"{parametro_enviado}",
                flush=True
            )

            raise Exception(
                f"El parámetro '{parametro_enviado}' "
                f"no pertenece al procedimiento."
            )

        print(
            "[VALIDACION] Parámetro válido: "
            f"{parametro_enviado}",
            flush=True
        )

    # =========================================================
    # FIN
    # =========================================================

    print(
        "\n[VALIDACION] Validación completada correctamente",
        flush=True
    )

    print(
        "[VALIDACION] Resultado final:",
        flush=True
    )

    print(
        f"[VALIDACION] parameter_placeholders = "
        f"{parameter_placeholders}",
        flush=True
    )

    print(
        f"[VALIDACION] parameter_values = "
        f"{parameter_values}",
        flush=True
    )

    print(
        "[VALIDACION] ANTES DEL RETURN",
        flush=True
    )

    resultado = (
        parameter_placeholders,
        parameter_values
    )

    print(
        "[VALIDACION] RESULTADO CONSTRUIDO",
        flush=True
    )

    print(
        f"[VALIDACION] Tipo resultado: "
        f"{type(resultado)}",
        flush=True
    )

    print(
        "[VALIDACION] DESPUÉS DE CONSTRUIR RESULTADO",
        flush=True
    )

    print(
        "[VALIDACION] validar_parametros() - FIN",
        flush=True
    )

    print("-" * 80, flush=True)

    print(
        "[VALIDACION] ANTES DE RETURN REAL",
        flush=True
    )

    return resultado