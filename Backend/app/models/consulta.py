from pydantic import BaseModel
from typing import Optional

class ConsultaIARequest(BaseModel):
    empresario_id: str
    pregunta: str

class ConsultaIAResponse(BaseModel):
    respuesta: str
    empresario_id: Optional[str] = None
    status: str = "success"
