def clasificar_documento(hallazgos: list[dict]) -> dict:

    tipos_detectados = {
        hallazgo["tipo"]
        for hallazgo in hallazgos
    }

    if "DNI" in tipos_detectados or "IBAN" in tipos_detectados:

        return {
            "clasificacion": "CONFIDENCIAL",
            "motivo": (
                "El documento contiene datos "
                "personales identificativos o financieros."
            )
        }

    if "EMAIL" in tipos_detectados or "TELEFONO" in tipos_detectados:

        return {
            "clasificacion": "INTERNO",
            "motivo": (
                "El documento contiene datos "
                "personales de contacto."
            )
        }

    return {
        "clasificacion": "PUBLICO",
        "motivo": (
            "No se han detectado patrones "
            "de información personal definidos."
        )
    }