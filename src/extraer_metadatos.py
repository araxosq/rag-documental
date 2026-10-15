import truststore
truststore.inject_into_ssl()

import os
from pathlib import Path

import fitz
from dotenv import load_dotenv
from google import genai

import json
from modelos import ContratoMetadata

import time

#Para mejorar el modelo y que las fechas no sean texto
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from datos_prueba import datos_prueba

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def leer_pdf(ruta_pdf):
    documento = fitz.open(ruta_pdf)

    texto = ""

    for pagina in documento:
        texto += pagina.get_text()

    return texto


ruta = Path("docs/contrato_prueba_ficticio.pdf")

texto = leer_pdf(ruta)

class Confidencialidad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class ContratoMetadata(BaseModel):
    tipo_documento: str = Field(
        min_length=3,
        description="Tipo de documento identificado"
    )

    cliente: Optional[str] = None
    proveedor: Optional[str] = None

    importe: Optional[float] = Field(
        default=None,
        ge=0,
        description="Importe total del contrato"
    )

    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    sla: Optional[str] = None

    confidencialidad: Optional[Confidencialidad] = None

    @field_validator("importe", mode="before")
    @classmethod
    def normalizar_importe(cls, valor):
        if valor is None:
            return None

        if isinstance(valor, (int, float)):
            return valor

        valor = str(valor).strip().upper()

        valor = valor.replace("EUR", "")
        valor = valor.replace("€", "")
        valor = valor.strip()

        # Formato europeo: 120.000,00
        if "." in valor and "," in valor:
            valor = valor.replace(".", "")
            valor = valor.replace(",", ".")

        # Formato: 120000,00
        elif "," in valor:
            valor = valor.replace(",", ".")

        return float(valor)

    @field_validator("confidencialidad", mode="before")
    @classmethod
    def normalizar_confidencialidad(cls, valor):
        if valor is None:
            return None

        valor = str(valor).strip().upper()

        equivalencias = {
            "BAJO": "BAJA",
            "BAJA": "BAJA",
            "MEDIO": "MEDIA",
            "MEDIA": "MEDIA",
            "ALTO": "ALTA",
            "ALTA": "ALTA",
        }

        return equivalencias.get(valor, valor)

    @field_validator("fecha_fin")
    @classmethod
    def validar_fechas(cls, fecha_fin, info):
        fecha_inicio = info.data.get("fecha_inicio")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError(
                "La fecha_fin no puede ser anterior a fecha_inicio"
            )

        return fecha_fin

prompt = f"""
Analiza el siguiente documento.

Extrae únicamente la información que aparezca explícitamente.

Devuelve los siguientes campos:

- tipo_documento
- cliente
- proveedor
- importe
- fecha_inicio
- fecha_fin
- sla
- confidencialidad

Si un dato no aparece, devuelve null.

Devuelve únicamente JSON válido.

DOCUMENTO:

{texto}
"""

#respuesta = client.models.generate_content(
#    model="gemini-3.8-flash",
#    contents=prompt
#)
respuesta = None
respuesta_texto = None
for intento in range(3):
    try:
        respuesta = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if respuesta.text:
            respuesta_texto = respuesta.text.strip()
            break

    except Exception as e:
        print(f"Intento {intento + 1} fallido: {e}")
        # Si la cuota está agotada, no tiene sentido reintentar
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            raise RuntimeError(
                "Cuota de Gemini agotada. Espera al reinicio de cuota o usa otro modelo."
            )

    if intento < 2:
        espera = 5 * (intento + 1)
        print(f"Esperando {espera} segundos...")
        time.sleep(espera)

#print(respuesta.text)

#datos = json.loads(respuesta.text)
datos = datos_prueba

if respuesta is not None and respuesta.text:
    respuesta_texto = respuesta.text.strip()

if not respuesta_texto:
    raise RuntimeError(
        "No se pudo obtener una respuesta válida de Gemini después de 3 intentos."
    )

respuesta_texto = respuesta_texto.replace("```json", "")
respuesta_texto = respuesta_texto.replace("```", "")
respuesta_texto = respuesta_texto.strip()

print("\nRESPUESTA BRUTA DE GEMINI:\n")
print(respuesta_texto)

#para jugar con los datos de prueba mientras no puedo hacer llamadas al modelo de Gemini
#datos = json.loads(respuesta_texto)


contrato = ContratoMetadata(**datos)

print("\nMETADATOS VALIDADOS:\n")
print(contrato)

# vuelca los metadatos en json
ruta_salida = ruta.with_suffix(".metadata.json")

with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(
        contrato.model_dump_json(
            indent=2
        )
    )

print(f"\nMetadatos guardados en: {ruta_salida}")