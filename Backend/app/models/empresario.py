from pydantic import BaseModel
from typing import Optional

class EmpresarioBase(BaseModel):
    id: str
    cedula: str
    nombre: str
    empresa: Optional[str] = "Sin Registro de Empresa"
    sector: Optional[str] = "Por Definir"

class EmpresarioResponse(EmpresarioBase):
    tiene_bitacora: bool = False
    archivo_bitacora: Optional[str] = None
    bitacora_file_id: Optional[str] = None
