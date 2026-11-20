from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.empresario import EmpresarioResponse, SincronizacionResponse
from app.services.data_pipeline_service import data_pipeline_service

router = APIRouter(prefix="/api", tags=["Empresarios"])

@router.get("/empresarios", response_model=SincronizacionResponse)
def listar_empresarios(force: bool = Query(False, description="Forzar actualización desde Google Drive")):
    """
    Obtiene el catálogo de empresarios con estado de bitácoras.
    Utiliza caché en memoria (TTL: 10 min) a menos que se especifique force=True.
    """
    try:
        return data_pipeline_service.obtener_catalogo_empresarios(forzar=force)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en pipeline de datos: {str(e)}")

@router.post("/empresarios/sincronizar", response_model=SincronizacionResponse)
def forzar_sincronizacion():
    """
    Invalida la caché en memoria y fuerza la re-sincronización con Google Drive.
    """
    try:
        return data_pipeline_service.obtener_catalogo_empresarios(forzar=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al forzar sincronización: {str(e)}")

@router.get("/empresarios/{id_o_cedula}", response_model=EmpresarioResponse)
def obtener_detalle_empresario(id_o_cedula: str):
    """
    Obtiene los datos y el estado del archivo de un empresario específico por ID o Cédula.
    """
    empresario = data_pipeline_service.obtener_empresario_por_id(id_o_cedula)
    if not empresario:
        raise HTTPException(status_code=404, detail=f"Empresario con ID o Cédula '{id_o_cedula}' no encontrado.")
    return empresario
