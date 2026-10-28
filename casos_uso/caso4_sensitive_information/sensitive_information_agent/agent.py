import sys
from pathlib import Path

from google.adk.agents import Agent


# Añadimos la raíz del proyecto al path para poder importar src
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from src.sensibilidad.detector import detectar_informacion_sensible
from src.sensibilidad.clasificador import clasificar_documento
from src.sensibilidad.decision import decidir_accion
from src.sensibilidad.anonimizador import anonimizar_texto
from src.sensibilidad.extractor_demo import extraer_documento


root_agent = Agent(
    name="sensitive_information_agent",
    #model="gemini-3.6-flash",
    model="gemini-3.5-flash-lite",

    description="""
    Agente especializado en gobierno y protección de información sensible.
    """,

    instruction="""
    Eres un agente especializado en gobierno y protección de información sensible.

    Puedes analizar tanto textos proporcionados por el usuario como documentos PDF
    almacenados localmente.

    Si el usuario proporciona una ruta a un PDF:

    1. Utiliza extraer_documento para obtener el texto.
    2. Utiliza detectar_informacion_sensible sobre el texto extraído.
    3. Utiliza clasificar_documento con los hallazgos obtenidos.
    4. Utiliza decidir_accion con la clasificación obtenida.
    5. Si la decisión indica que requiere anonimización,
    utiliza anonimizar_texto.

    Debes seguir este flujo:

    EXTRACT → DETECT → CLASSIFY → DECIDE → PROTECT

    No inventes resultados.
    Utiliza siempre los resultados proporcionados por las herramientas.

    Presenta finalmente:
    - Información sensible detectada.
    - Clasificación.
    - Motivo.
    - Decisión.
    - Si puede compartirse.
    - Si requiere anonimización.
    - Texto anonimizado cuando corresponda.
    """,

    tools=[
        detectar_informacion_sensible,
        clasificar_documento,
        decidir_accion,
        anonimizar_texto,
        extraer_documento
    ]
)