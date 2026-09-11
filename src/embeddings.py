import truststore
truststore.inject_into_ssl()

import pymupdf
from pathlib import Path
from sentence_transformers import SentenceTransformer

import pymupdf
from pathlib import Path
from sentence_transformers import SentenceTransformer

#ruta = Path("documentos/SDD_Manual_ArquitecturaDatos.pdf")
ruta = Path("documentos/documento_prueba_rag.pdf")

TAMANO_CHUNK = 500
SOLAPE = 100

documento = pymupdf.open(ruta)

chunks = []

for numero_pagina, pagina in enumerate(documento, start=1):
    texto = pagina.get_text().strip()

    if not texto:
        continue

    inicio = 0

    while inicio < len(texto):
        fin = inicio + TAMANO_CHUNK
        fragmento = texto[inicio:fin]

        chunks.append({
            "documento": ruta.name,
            "pagina": numero_pagina,
            "texto": fragmento
        })

        inicio += TAMANO_CHUNK - SOLAPE

print(f"Chunks creados: {len(chunks)}")

print("Cargando modelo de embeddings...")

modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [chunk["texto"] for chunk in chunks]

print("Generando embeddings...")

embeddings = modelo.encode(textos)

print("Embeddings generados correctamente")
print("Número de embeddings:", len(embeddings))
print("Dimensiones de cada vector:", len(embeddings[0]))

print("\nEjemplo de vector:")
print(embeddings[0][:20])