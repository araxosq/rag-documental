import truststore
truststore.inject_into_ssl()

import pymupdf
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np
import requests


# --------------------------------
# CONFIGURACIÓN
# --------------------------------

ruta = Path("documentos/documento_prueba_rag.pdf")

TAMANO_MAX_CHUNK = 800
TOP_K = 3

PESO_SEMANTICO = 0.70
PESO_BM25 = 0.30

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODELO_LLM = "qwen3-4b-instruct-2507"


# --------------------------------
# 1. LEER DOCUMENTO
# --------------------------------

documento = pymupdf.open(ruta)

chunks = []

for numero_pagina, pagina in enumerate(documento, start=1):

    texto = pagina.get_text().strip()

    if not texto:
        continue

    parrafos = [
        p.strip()
        for p in texto.split("\n")
        if len(p.strip()) > 40
    ]

    chunk_actual = ""

    for parrafo in parrafos:

        if len(chunk_actual) + len(parrafo) <= TAMANO_MAX_CHUNK:

            chunk_actual += " " + parrafo

        else:

            if chunk_actual.strip():

                chunks.append({
                    "documento": ruta.name,
                    "pagina": numero_pagina,
                    "texto": chunk_actual.strip()
                })

            chunk_actual = parrafo

    if chunk_actual.strip():

        chunks.append({
            "documento": ruta.name,
            "pagina": numero_pagina,
            "texto": chunk_actual.strip()
        })


print(f"Chunks creados: {len(chunks)}")


# --------------------------------
# 2. EMBEDDINGS
# --------------------------------

print("Cargando modelo de embeddings...")

modelo_embeddings = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [
    chunk["texto"]
    for chunk in chunks
]

print("Generando embeddings...")

embeddings_documentos = modelo_embeddings.encode(
    textos,
    normalize_embeddings=True
)


# --------------------------------
# 3. BM25
# --------------------------------

textos_tokenizados = [
    texto.lower().split()
    for texto in textos
]

bm25 = BM25Okapi(
    textos_tokenizados
)


# --------------------------------
# 4. PREGUNTA
# --------------------------------

pregunta = input(
    "\nEscribe tu pregunta: "
)


# --------------------------------
# 5. BÚSQUEDA SEMÁNTICA
# --------------------------------

embedding_pregunta = modelo_embeddings.encode(
    [pregunta],
    normalize_embeddings=True
)

scores_semanticos = cosine_similarity(
    embedding_pregunta,
    embeddings_documentos
)[0]


# --------------------------------
# 6. BM25
# --------------------------------

pregunta_tokenizada = (
    pregunta
    .lower()
    .split()
)

scores_bm25 = bm25.get_scores(
    pregunta_tokenizada
)

if scores_bm25.max() > 0:

    scores_bm25 = (
        scores_bm25 /
        scores_bm25.max()
    )


# --------------------------------
# 7. COMBINAR SCORES
# --------------------------------

scores_finales = (
    PESO_SEMANTICO * scores_semanticos
    +
    PESO_BM25 * scores_bm25
)

indices = np.argsort(
    scores_finales
)[::-1][:TOP_K]


# --------------------------------
# 8. CREAR CONTEXTO
# --------------------------------

contexto = ""

fuentes = []

for indice in indices:

    chunk = chunks[indice]

    contexto += (
        f"\nDOCUMENTO: {chunk['documento']}\n"
        f"PÁGINA: {chunk['pagina']}\n"
        f"TEXTO:\n{chunk['texto']}\n"
        f"{'-' * 60}\n"
    )

    fuentes.append(
        f"{chunk['documento']} - página {chunk['pagina']}"
    )


# --------------------------------
# 9. PROMPT
# --------------------------------

prompt = f"""
Eres un asistente especializado en gestión documental.

Debes responder únicamente utilizando la información
contenida en el CONTEXTO.

Reglas:

1. No inventes información.
2. Si la respuesta no aparece en el contexto, responde:
   "No encuentro esa información en los documentos disponibles."
3. Responde de forma clara y concisa.
4. No utilices conocimiento externo.
5. Indica la fuente y la página cuando corresponda.

CONTEXTO:

{contexto}

PREGUNTA:

{pregunta}
"""


# --------------------------------
# 10. LLAMAR A LM STUDIO
# --------------------------------

payload = {
    "model": MODELO_LLM,
    "messages": [
        {
            "role": "system",
            "content": (
                "Eres un asistente documental. "
                "Solo puedes responder usando "
                "el contexto proporcionado."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.1
}


print("\nConsultando el LLM...\n")

respuesta = requests.post(
    LM_STUDIO_URL,
    json=payload,
    timeout=120
)

respuesta.raise_for_status()

datos = respuesta.json()

respuesta_final = (
    datos["choices"][0]
    ["message"]
    ["content"]
)


# --------------------------------
# 11. MOSTRAR RESPUESTA
# --------------------------------

print("=" * 70)
print("RESPUESTA DEL RAG")
print("=" * 70)

print(respuesta_final)


print("\n" + "=" * 70)
print("FRAGMENTOS RECUPERADOS")
print("=" * 70)

for i, indice in enumerate(
    indices,
    start=1
):

    chunk = chunks[indice]

    print(
        f"\n{i}. "
        f"{chunk['documento']} "
        f"- página {chunk['pagina']}"
    )

    print(
        f"Score: "
        f"{scores_finales[indice]:.3f}"
    )