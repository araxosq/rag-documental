from detector import detectar_informacion_sensible
from clasificador import clasificar_documento
from decision import decidir_accion
from anonimizador import anonimizar_texto


# ============================================================
# TEXTO DE PRUEBA
# ============================================================

texto = """
El titular Juan Pérez con DNI 12345678Z solicita que el pago
se realice en el IBAN ES12 1234 5678 9012 3456 7890.

Para cualquier comunicación puede utilizarse el correo
juan.perez@gmail.com o el teléfono +34 612 345 678.
"""


print("\n==========================================")
print(" SENSITIVE INFORMATION DETECTOR")
print(" PRUEBA LOCAL - SIN AGENTE")
print("==========================================")

print("\n--- TEXTO ORIGINAL ---")
print(texto)


# ============================================================
# 1. DETECT
# ============================================================

hallazgos = detectar_informacion_sensible(texto)

print("\n--- 1. DETECCIÓN ---")

if hallazgos:
    for hallazgo in hallazgos:
        print(
            f"{hallazgo['tipo']}: "
            f"{hallazgo['valor']}"
        )
else:
    print("No se ha detectado información sensible.")


# ============================================================
# 2. CLASSIFY
# ============================================================

clasificacion = clasificar_documento(hallazgos)

print("\n--- 2. CLASIFICACIÓN ---")
print("Nivel:", clasificacion["clasificacion"])
print("Motivo:", clasificacion["motivo"])


# ============================================================
# 3. DECIDE
# ============================================================

decision = decidir_accion(clasificacion)

print("\n--- 3. DECISIÓN ---")
print("Acción:", decision["accion"])
print("¿Puede compartirse?:", decision["compartir"])
print(
    "¿Requiere anonimización?:",
    decision["requiere_anonimizacion"]
)
print("Motivo:", decision["motivo"])


# ============================================================
# 4. PROTECT
# ============================================================

print("\n--- 4. PROTECCIÓN ---")

if decision["requiere_anonimizacion"]:

    resultado = anonimizar_texto(
        texto,
        hallazgos
    )

    print(resultado["texto_anonimizado"])

    print(
        "\nElementos anonimizados:",
        resultado["elementos_anonimizados"]
    )

else:
    print("El documento no requiere anonimización.")


print("\n==========================================")
print(" FIN DEL ANÁLISIS")
print("==========================================")