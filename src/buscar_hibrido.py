import truststore
truststore.inject_into_ssl()

import pymupdf
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np

ruta = Path("documentos/SDD_Manual_ArquitecturaDatos.pdf")

TAMANO_MAX_CHUNK = 800
TOP_K = 5

# Peso de cada tipo de búsqueda
PESO_SEMANTICO = 0.70
PESO_BM25 = 0.30


# --------------------------------
# 1. LEER PDF Y CREAR CHUNKS
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

modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [chunk["texto"] for chunk in chunks]

print("Generando embeddings...")

embeddings = modelo.encode(
    textos,
    normalize_embeddings=True
)


# --------------------------------
# 3. PREPARAR BM25
# --------------------------------

textos_tokenizados = [
    texto.lower().split()
    for texto in textos
]

bm25 = BM25Okapi(textos_tokenizados)


# --------------------------------
# 4. PREGUNTA
# --------------------------------

pregunta = input("\nEscribe tu pregunta: ")


# --------------------------------
# 5. BÚSQUEDA SEMÁNTICA
# --------------------------------

embedding_pregunta = modelo.encode(
    [pregunta],
    normalize_embeddings=True
)

scores_semanticos = cosine_similarity(
    embedding_pregunta,
    embeddings
)[0]


# --------------------------------
# 6. BÚSQUEDA BM25
# --------------------------------

pregunta_tokenizada = pregunta.lower().split()

scores_bm25 = bm25.get_scores(
    pregunta_tokenizada
)


# --------------------------------
# 7. NORMALIZAR BM25
# --------------------------------

if scores_bm25.max() > 0:

    scores_bm25 = (
        scores_bm25 /
        scores_bm25.max()
    )


# --------------------------------
# 8. COMBINAR RESULTADOS
# --------------------------------

scores_finales = (
    PESO_SEMANTICO * scores_semanticos
    +
    PESO_BM25 * scores_bm25
)


# --------------------------------
# 9. TOP K
# --------------------------------

indices = np.argsort(
    scores_finales
)[::-1][:TOP_K]


# --------------------------------
# 10. MOSTRAR RESULTADOS
# --------------------------------

print("\nRESULTADOS HYBRID SEARCH\n")

for posicion, indice in enumerate(indices, start=1):

    chunk = chunks[indice]

    print("=" * 70)

    print(f"RESULTADO {posicion}")

    print(
        f"Score final: "
        f"{scores_finales[indice]:.3f}"
    )

    print(
        f"Semántico: "
        f"{scores_semanticos[indice]:.3f}"
    )

    print(
        f"BM25: "
        f"{scores_bm25[indice]:.3f}"
    )

    print(f"Documento: {chunk['documento']}")
    print(f"Página: {chunk['pagina']}")

    print("-" * 70)

    print(chunk["texto"])

    print()