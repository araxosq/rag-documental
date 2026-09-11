import pymupdf
from pathlib import Path

#ruta = Path("documentos/SDD_Manual_ArquitecturaDatos.pdf")
ruta = Path("documentos/documento_prueba_rag.pdf")

documento = pymupdf.open(ruta)

print(f"Documento: {ruta.name}")
print(f"Número de páginas: {len(documento)}")

for numero_pagina, pagina in enumerate(documento, start=1):

    texto = pagina.get_text()

    print("\n" + "=" * 50)
    print(f"PÁGINA {numero_pagina}")
    print("=" * 50)

    print(texto[:1000])