import pymupdf
from pathlib import Path

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

print(f"Total de chunks creados: {len(chunks)}")

for i, chunk in enumerate(chunks[:5], start=1):
    print("\n" + "=" * 60)
    print(f"CHUNK {i}")
    print(f"Documento: {chunk['documento']}")
    print(f"Página: {chunk['pagina']}")
    print("-" * 60)
    print(chunk["texto"])