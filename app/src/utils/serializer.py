def serialize_rows(result: dict) -> dict:
    """
    Recibe el resultado de execute_query()
    y lo convierte en una lista de diccionarios.
    """

    print("\n" + "-" * 80)
    print("[SERIALIZER] INICIO")
    print("-" * 80)

    print("[SERIALIZER] Obteniendo has_data...")
    has_data = result["has_data"]
    print(f"[SERIALIZER] has_data: {has_data}")

    print("[SERIALIZER] Obteniendo metadata...")
    metadata = result["metadata"]
    print(f"[SERIALIZER] metadata obtenida. Columnas: {len(metadata)}")

    print("[SERIALIZER] Obteniendo rows...")
    rows = result["rows"]
    print(f"[SERIALIZER] rows obtenidas. Cantidad: {len(rows)}")

    print("[SERIALIZER] Obteniendo message...")
    mensaje = result["message"]
    print(f"[SERIALIZER] message: {mensaje}")

    # ---------------------------------------------------------
    # Construir nombres de columnas
    # ---------------------------------------------------------

    print("[SERIALIZER] Construyendo columnas...")

    columnas = [
        columna[0] for columna in metadata
    ]

    print(f"[SERIALIZER] COLUMNAS: {columnas}")

    # ---------------------------------------------------------
    # Convertir filas a diccionarios
    # ---------------------------------------------------------

    print("[SERIALIZER] Construyendo data...")

    data = [
        dict(zip(columnas, row))
        for row in rows
    ]

    print(
        f"[SERIALIZER] data construida. "
        f"Cantidad de registros: {len(data)}"
    )

    # ---------------------------------------------------------
    # Resultado final
    # ---------------------------------------------------------

    resultado = {
        "has_data": has_data,
        "message": mensaje,
        "data": data
    }

    print("[SERIALIZER] Resultado construido correctamente")
    print("[SERIALIZER] FIN")
    print("-" * 80)

    return resultado