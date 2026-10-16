import json
from datetime import date
from pathlib import Path

def leer_todos_los_metadatos(carpeta: str) -> list[dict]:
    """
    Lee todos los archivos *.metadata.json de una carpeta
    y devuelve una lista de contratos.
    """

    ruta_carpeta = Path(carpeta)

    contratos = []

    for archivo in ruta_carpeta.glob("*.metadata.json"):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        datos["_archivo_metadata"] = str(archivo)

        contratos.append(datos)

    return contratos

def leer_metadatos(ruta_json):
    ruta = Path(ruta_json)

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def dias_hasta_vencimiento(fecha_fin):
    fecha = date.fromisoformat(fecha_fin)
    return (fecha - date.today()).days

from src.rag import consultar_rag


def consultar_contrato_rag(pregunta: str) -> str:
    """
    Consulta el contenido completo del contrato mediante RAG.
    Úsala cuando la información no esté disponible en los metadatos,
    especialmente para cláusulas, renovaciones, preavisos y obligaciones.
    """

    return consultar_rag(pregunta)

from datetime import date


def contratos_por_vencer(
    contratos: list[dict],
    dias_limite: int = 90
) -> list[dict]:
    """
    Devuelve los contratos que vencen dentro del número
    de días indicado.
    """

    resultado = []

    hoy = date.today()

    for contrato in contratos:
        fecha_fin = contrato.get("fecha_fin")

        if not fecha_fin:
            continue

        fecha = date.fromisoformat(fecha_fin)

        dias_restantes = (fecha - hoy).days

        if 0 <= dias_restantes <= dias_limite:
            contrato_copia = contrato.copy()
            contrato_copia["dias_restantes"] = dias_restantes
            resultado.append(contrato_copia)

    return resultado