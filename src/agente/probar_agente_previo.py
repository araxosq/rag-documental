from pathlib import Path

from tools import leer_metadatos, dias_hasta_vencimiento


ruta = Path("docs/contrato_prueba.metadata.json")

metadata = leer_metadatos(ruta)

dias = dias_hasta_vencimiento(metadata["fecha_fin"])

print("\nREVISION DE CONTRATO\n")

print("Tipo:", metadata["tipo_documento"])
print("Proveedor:", metadata["proveedor"])
print("Fecha fin:", metadata["fecha_fin"])
print("Dias hasta vencimiento:", dias)

if dias < 0:
    print("Estado: VENCIDO")

elif dias <= 90:
    print("Estado: REQUIERE REVISION")

else:
    print("Estado: VIGENTE")