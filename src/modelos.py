from typing import Optional
from pydantic import BaseModel


from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


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