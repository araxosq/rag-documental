import truststore
truststore.inject_into_ssl()

import pymupdf
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ruta = Path("documentos/SDD_Manual_ArquitecturaDatos.pdf")

TAMANO_MAX_CHUNK = 800
TOP_K = 5
UMBRAL_SIMILITUD = 0.35

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

print("Cargando modelo...")

modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [chunk["texto"] for chunk in chunks]

print("Generando embeddings...")

embeddings_documentos = modelo.encode(
    textos,
    normalize_embeddings=True
)

pregunta = input("\nEscribe tu pregunta: ")

embedding_pregunta = modelo.encode(
    [pregunta],
    normalize_embeddings=True
)

similitudes = cosine_similarity(
    embedding_pregunta,
    embeddings_documentos
)[0]

indices = similitudes.argsort()[::-1]

print("\nRESULTADOS MÁS RELEVANTES\n")

resultados_mostrados = 0

for indice in indices:

    if similitudes[indice] < UMBRAL_SIMILITUD:
        continue

    chunk = chunks[indice]

    resultados_mostrados += 1

    print("=" * 70)
    print(f"RESULTADO {resultados_mostrados}")
    print(f"Similitud: {similitudes[indice]:.3f}")
    print(f"Documento: {chunk['documento']}")
    print(f"Página: {chunk['pagina']}")
    print("-" * 70)
    print(chunk["texto"])
    print()

    if resultados_mostrados >= TOP_K:
        break


if resultados_mostrados == 0:
    print("No se han encontrado fragmentos suficientemente relevantes.")