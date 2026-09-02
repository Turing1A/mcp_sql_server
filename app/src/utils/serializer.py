def serialize_rows(result: dict) -> dict:
    """
    Recibe el resultado de execute_query()
    y lo convierte en una lista de diccionarios.
    """

    has_data = result["has_data"]
    metadata = result["metadata"]
    rows = result["rows"]
    mensaje = result["message"]

    # ---------------------------------------------------------
    # Construir nombres de columnas
    # ---------------------------------------------------------

    columnas = [
        columna[0] for columna in metadata
    ]

    # ---------------------------------------------------------
    # Convertir filas a diccionarios
    # ---------------------------------------------------------

    data = [
        dict(zip(columnas, row))
        for row in rows
    ]

    # ---------------------------------------------------------
    # Resultado final
    # ---------------------------------------------------------

    resultado = {
        "has_data": has_data,
        "message": mensaje,
        "data": data
    }

    return resultado