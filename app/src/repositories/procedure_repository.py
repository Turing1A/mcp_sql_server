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

    resultado = execute_query(
        sql,
        parameters
    )

    resultado_serializado = serialize_rows(resultado)

    return resultado_serializado


# -----------------------------------------------------------------------
# GET PROCEDURES
# -----------------------------------------------------------------------
def get_procedures(userID: int):



    sql = """
        EXEC bi.mcp_listar_sp ?
    """

    resultado = execute_query(sql, (userID,))

    resultado_serializado = serialize_rows(resultado)



    return resultado_serializado

# -----------------------------------------------------------------------
# AUTENTICATE USER
# -----------------------------------------------------------------------
# def aut_user(userID: int):

#     sql = """
#         EXEC bi.authentication ?
#     """



#     resultado = execute_query(sql, (userID,))

#     resultado_serializado = serialize_rows(resultado)



#     return resultado_serializado


# -----------------------------------------------------------------------
# TEST CONNECTION
# -----------------------------------------------------------------------
def get_test_connection():



    sql = """
        SELECT DB_NAME()
    """

    resultado = execute_query(sql)

    resultado_serializado = serialize_rows(resultado)

  

    return resultado_serializado


# -----------------------------------------------------------------------
# GET PROCEDURE DETAILS
# -----------------------------------------------------------------------
def get_procedure_details(
    procedure_name: str
):



    sql = """
        EXEC bi.mcp_descripcion_sp ?
    """

    resultado = execute_query(
        sql,
        (procedure_name,)
    )

    if not resultado['has_data']:
        
        raise Exception(
            f"No existe información para el sp "
            f"'{procedure_name}'."
        )

    resultado_serializado = serialize_rows(resultado)

    rows = resultado_serializado["data"]

    # ---------------------------------------------------------
    # Construir definición
    # ---------------------------------------------------------

    procedure = {
        "schema": rows[0]["schema_name"],
        "proc_almacenado": rows[0]["proc_almacenado"],
        "descripcion": rows[0]["descripcion_parametro"],
        "use_cases": rows[0]["use_cases"],
        "parameters": []
    }

    # ---------------------------------------------------------
    # Construir parámetros
    # ---------------------------------------------------------

    for row in rows:
        procedure["parameters"].append(
            {
                "name": row["parameter_name"],
                "type": row["parameter_type"],
                "required": row["required"],
                "example": row["example"],
                "orden": row["orden"]
            }
        )



    return procedure


# -----------------------------------------------------------------------
# EXECUTE PROCEDURE
# -----------------------------------------------------------------------
def execute_procedure(
    procedure_name: str,
    parametros_enviados: dict | None = None
):


    # ---------------------------------------------------------
    # Normalizar None
    # ---------------------------------------------------------

    if parametros_enviados is None:
        parametros_enviados = {}

    sql = """
        SELECT bi.CONSULTAR_PROCEDIMIENTO_EXISTENTE(?)
    """

    try:

        # =====================================================
        # PASO 1
        # =====================================================

        resultado = execute_and_serialize(
            sql,
            (procedure_name,)
        )

        if not resultado["has_data"]:

            raise Exception(
                f"El procedimiento '{procedure_name}' "
                f"no existe o no está habilitado."
            )

        # =====================================================
        # PASO 2
        # =====================================================

        
        procedure_definition = get_procedure_details(
            procedure_name
        )

        parametros_catalogo = (
            procedure_definition["parameters"]
        )

        schema = procedure_definition["schema"]

        # =====================================================
        # PASO 3
        # =====================================================

        if not parametros_catalogo:

            sql = f"""
                EXEC {schema}.{procedure_name}
            """

            resultado = execute_and_serialize(sql)

            return resultado

        # =====================================================
        # PASO 4
        # =====================================================

   

        resultado_validacion = validar_parametros(
            parametros_catalogo,
            parametros_enviados
        )

        parameter_placeholders, parameter_values = (
            resultado_validacion
        )

        # =====================================================
        # PASO 5
        # =====================================================

        sql = f"""
            EXEC {schema}.{procedure_name}
            {', '.join(parameter_placeholders)}
        """
        print("sql",sql)
        # =====================================================
        # PASO 6
        # =====================================================



        resultado = execute_and_serialize(
            sql,
            tuple(parameter_values)
        )


        return resultado

    except Exception as e:

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

    parameter_placeholders = []
    parameter_values = []
    parametros_validos = set()

    # =========================================================
    # FOR CATÁLOGO
    # =========================================================

    for indice, parametro in enumerate(
        parametros_catalogo,
        start=1
    ):

        # Obtener nombre
        nombre_parametro_catalogo = parametro["name"]

        nombre_parametro_catalogo = (
            nombre_parametro_catalogo.replace("@", "")
        )

        # Parámetros válidos
        parametros_validos.add(
            nombre_parametro_catalogo
        )

        # Verificar si fue enviado
        if nombre_parametro_catalogo not in parametros_enviados:

            required = parametro["required"]

            if required:
                raise Exception(
                    f"Falta el parámetro obligatorio "
                    f"'{nombre_parametro_catalogo}'."
                )

            continue

        # Parámetro enviado

        # Placeholder
        placeholder = (
            f"@{nombre_parametro_catalogo}=?"
        )

        parameter_placeholders.append(
            placeholder
        )

        # Valor
        valor = parametros_enviados[
            nombre_parametro_catalogo
        ]

        parameter_values.append(valor)

    # =========================================================
    # FIN FOR
    # =========================================================

   

    resultado = (
        parameter_placeholders,
        parameter_values
    )

    return resultado