from pydantic import BaseModel
from typing import Optional

class ConsultaIARequest(BaseModel):
    empresario_id: str
    pregunta: str
    tipo_analisis: Optional[str] = "general"  # "ventas" | "costos" | "plan_accion" | "riesgos" | "general"

class ConsultaIAResponse(BaseModel):
    respuesta: str
    empresario_id: Optional[str] = None
    tipo_analisis: Optional[str] = "general"
    contexto_utilizado: Optional[str] = None
    modelo: Optional[str] = "gemini-1.5-flash"
    status: str = "success"
