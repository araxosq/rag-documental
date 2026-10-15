from pathlib import Path

from modelos import ContratoMetadata


datos_prueba = {
    "tipo_documento": "Contrato de prestación de servicios tecnológicos",
    "cliente": "ACME Retail España, S.A.",
    "proveedor": "CloudData Solutions, S.L.",
    "importe": "120.000,00 EUR",
    "fecha_inicio": "2026-02-01",
    "fecha_fin": "2027-01-31",
    "sla": "99.90% disponibilidad mensual; respuesta Sev1 30 min; resolución objetivo 4 h",
    "confidencialidad": "ALTO"
}


contrato = ContratoMetadata(**datos_prueba)

print("\nMETADATOS VALIDADOS:\n")
print(contrato)


ruta_salida = Path("docs/contrato_prueba.metadata.json")

with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(
        contrato.model_dump_json(indent=2)
    )

print(f"\nMetadatos guardados en: {ruta_salida}")