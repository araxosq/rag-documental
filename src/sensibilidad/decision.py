def decidir_accion(clasificacion: dict) -> dict:

    nivel = clasificacion["clasificacion"]

    if nivel == "CONFIDENCIAL":
        return {
            "accion": "PROTEGER",
            "compartir": False,
            "requiere_anonimizacion": True,
            "motivo": (
                "El documento contiene información confidencial "
                "y debe protegerse antes de compartirse."
            )
        }

    if nivel == "INTERNO":
        return {
            "accion": "RESTRINGIR",
            "compartir": False,
            "requiere_anonimizacion": False,
            "motivo": (
                "El documento contiene información de uso interno."
            )
        }

    return {
        "accion": "PERMITIR",
        "compartir": True,
        "requiere_anonimizacion": False,
        "motivo": "No se ha detectado información sensible."
    }