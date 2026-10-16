import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agente import agente


APP_NAME = "revision_contratos"
USER_ID = "usuario_prueba"
SESSION_ID = "sesion_1"


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=agente,
        app_name=APP_NAME,
        session_service=session_service,
    )

    mensaje = types.Content(
        role="user",
        parts=[
            types.Part(
                    text=(
                        "Revisa todos los contratos de la carpeta 'documentos'. "
                        "Identifica cuáles vencen en los próximos 120 días. "
                        "Distingue entre contratos vencidos, próximos a vencer y vigentes. "
                        "Para los contratos próximos a vencer, revisa si existen cláusulas "
                        "de renovación, prórroga o preaviso y genera un informe priorizado "
                        "con las actuaciones recomendadas."
                    )
            )
        ],
    )

    events = runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=mensaje,
    )

    async for event in events:
        if event.is_final_response():
            print("\nRESPUESTA DEL AGENTE:\n")

            if event.content and event.content.parts:
                for part in event.content.parts:
                    if getattr(part, "text", None):
                        print(part.text)
            else:
                print("El agente terminó sin devolver contenido de texto.")


if __name__ == "__main__":
    asyncio.run(main())