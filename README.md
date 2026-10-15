# Gestor Documental con IA

Prototipo de gestor documental inteligente orientado a aprender y construir
capacidades de IA sobre documentación no estructurada.

Actualmente el proyecto implementa dos casos de uso principales:

### Caso 1 - Consulta documental mediante RAG
Consulta inteligente sobre documentos PDF mediante chunking, embeddings, búsqueda híbrida y un LLM local.
[Ver Caso 1 - RAG documental](casos_uso/caso1_rag/README.md)

### Caso 2 - Extracción y gobierno de metadatos
Extracción de información desde documentos, normalización y validación con Pydantic y persistencia en JSON.
[Ver Caso 2 - Extracción de metadatos](casos_uso/caso2_metadatos/README.md)

## Seguridad
Si el repositorio es público:

No subir documentos corporativos o confidenciales.
No versionar .env ni credenciales.
No subir modelos .gguf.
No subir .venv.
Revisar git status antes de cada commit.
Utilizar documentos ficticios o públicos para las demostraciones.
El .gitignore debe configurarse antes de versionar archivos sensibles.

## Próximas mejoras
Posibles evoluciones:

Múltiples documentos.
Base vectorial persistente.
Filtros por metadatos.
Chunking basado en estructura y secciones.
Reranking.
Evaluación del retrieval y de las respuestas.
Extracción estructurada de metadatos.
Clasificación documental.
Interfaz con Streamlit.
Carga de documentos desde la aplicación.
Historial de conversaciones.
Usuarios y permisos.
Docker.
Arquitectura equivalente en GCP.
Objetivo de aprendizaje
El objetivo es comprender cada componente:

Ingesta -> Chunking -> Embeddings -> Retrieval -> Contexto -> LLM -> Respuesta
y poder evolucionar el prototipo hacia un gestor documental con IA.