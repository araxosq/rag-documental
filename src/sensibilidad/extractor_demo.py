from pathlib import Path
import fitz


def extraer_documento(ruta_documento: str) -> dict:
    """
    Extrae el texto de un documento PDF almacenado localmente.

    Args:
        ruta_documento: Ruta del archivo PDF.

    Returns:
        Diccionario con la ruta y el texto extraído.
    """

    ruta = Path(ruta_documento)

    if not ruta.exists():
        return {
            "error": f"No se encuentra el documento: {ruta_documento}"
        }

    if ruta.suffix.lower() != ".pdf":
        return {
            "error": "Actualmente solo se admiten documentos PDF."
        }

    documento = fitz.open(ruta)

    texto = ""

    for pagina in documento:
        texto += pagina.get_text() + "\n"

    documento.close()

    return {
        "ruta": str(ruta),
        "texto": texto
    }