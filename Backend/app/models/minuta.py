from pydantic import BaseModel
from typing import List, Optional

class TareaItem(BaseModel):
    id: str
    descripcion: str
    responsable: str  # "consultor" o "empresario"
    completada: bool = False
    fecha_limite: Optional[str] = "Próxima sesión (7 días)"
    enlace_whatsapp: Optional[str] = None

class MinutaVozRequest(BaseModel):
    empresario_id: str
    texto_dictado: str

class MinutaVozResponse(BaseModel):
    empresario_id: str
    nombre_empresario: str
    telefono_empresario: Optional[str] = None
    resumen_sesion: str
    tareas_consultor: List[TareaItem]
    tareas_empresario: List[TareaItem]
    status: str = "success"
