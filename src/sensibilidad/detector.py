import re


PATRONES = {
    "DNI": r"\b\d{8}[A-Za-z]\b",

    "EMAIL": (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "IBAN": (
        r"\bES\d{2}(?:\s?\d{4}){5}\b"
    ),

    "TELEFONO": (
        r"\b(?:\+34\s?)?"
        r"[6789]\d{8}\b"
    ),
}


def detectar_informacion_sensible(texto: str) -> list[dict]:
    hallazgos = []

    for tipo, patron in PATRONES.items():

        coincidencias = re.findall(
            patron,
            texto,
            flags=re.IGNORECASE
        )

        for valor in coincidencias:

            hallazgos.append({
                "tipo": tipo,
                "valor": valor
            })

    return hallazgos