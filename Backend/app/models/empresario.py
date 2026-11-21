from pydantic import BaseModel
from typing import Optional, List

class EmpresarioBase(BaseModel):
    id: str
    cedula: str
    nombre: str
    empresa: Optional[str] = "Sin Registro de Empresa"
    sector: Optional[str] = "Por Definir"
    telefono: Optional[str] = "3150000000"

class EmpresarioResponse(EmpresarioBase):
    tiene_bitacora: bool = False
    archivo_bitacora: Optional[str] = None
    bitacora_file_id: Optional[str] = None

class SincronizacionResponse(BaseModel):
    drive_status: str  # "connected" | "offline" | "api_disabled"
    mensaje: str
    ultima_sincronizacion: str
    total_empresarios: int
    empresarios: List[EmpresarioResponse]
