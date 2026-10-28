from .detector import detectar_informacion_sensible
from .clasificador import clasificar_documento


texto_prueba = """
Nombre: Ana García López
DNI: 12345678Z
Email: ana.garcia@empresa.com
Teléfono: 612345678
IBAN: ES12 1234 5678 9012 3456 7890
"""


hallazgos = detectar_informacion_sensible(
    texto_prueba
)

clasificacion = clasificar_documento(
    hallazgos
)


print("\nHALLAZGOS:\n")

for hallazgo in hallazgos:
    print(
        f"{hallazgo['tipo']}: "
        f"{hallazgo['valor']}"
    )


print("\nCLASIFICACION:\n")

print(
    clasificacion["clasificacion"]
)

print(
    clasificacion["motivo"]
)