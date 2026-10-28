def anonimizar_texto(texto: str, hallazgos: list[dict]) -> dict:
    """
    Anonimiza en un texto los datos sensibles previamente detectados.

    Args:
        texto: Texto original.
        hallazgos: Lista de datos sensibles detectados.

    Returns:
        Diccionario con el texto anonimizado y el número de
        elementos protegidos.
    """

    texto_anonimizado = texto

    for hallazgo in hallazgos:
        valor = hallazgo["valor"]
        tipo = hallazgo["tipo"]

        texto_anonimizado = texto_anonimizado.replace(
            valor,
            f"[{tipo}_ANONIMIZADO]"
        )

    return {
        "texto_anonimizado": texto_anonimizado,
        "elementos_anonimizados": len(hallazgos)
    }