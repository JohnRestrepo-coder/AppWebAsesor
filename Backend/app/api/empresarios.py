from fastapi import APIRouter, HTTPException
from typing import List
import re

try:
    from app.services.drive_service import drive_service
    from app.services.excel_service import excel_service
    from app.models.empresario import EmpresarioResponse
    from app.utils.constants import FOLDER_ASESORIAS_NAME, FOLDER_ASESORIAS_2026_NAME, FILE_LISTA_EMPRENDEDORES_NAME
except ImportError:
    from services.drive_service import drive_service
    from services.excel_service import excel_service
    from models.empresario import EmpresarioResponse
    FOLDER_ASESORIAS_NAME = "Asesorias"
    FOLDER_ASESORIAS_2026_NAME = "Asesorias_2026"
    FILE_LISTA_EMPRENDEDORES_NAME = "Lista Emprendedores.xlsx"

router = APIRouter(prefix="/api", tags=["Empresarios"])

@router.get("/empresarios", response_model=List[EmpresarioResponse])
def obtener_empresarios():
    """
    1. Carga la lista base desde 'Mi unidad/Asesorias/Lista Emprendedores.xlsx' (Hoja Emprendedores).
    2. Comprueba la existencia de la bitácora individual en 'Mi unidad/Asesorias/Asesorias_2026/'.
    3. Retorna la información estructurada para el Frontend.
    """
    try:
        # Paso 1: Obtener ID de carpeta contenedora 'Asesorias'
        id_folder_asesorias = drive_service.buscar_id_por_nombre(FOLDER_ASESORIAS_NAME, es_carpeta=True)

        # Paso 2: Descargar y procesar 'Lista Emprendedores.xlsx'
        id_excel_lista = drive_service.buscar_id_por_nombre(FILE_LISTA_EMPRENDEDORES_NAME, parent_id=id_folder_asesorias)
        bytes_lista = drive_service.descargar_archivo_bytes(id_excel_lista)
        lista_emprendedores = excel_service.procesar_hoja_emprendedores(bytes_lista)

        # Paso 3: Obtener ID de la subcarpeta 'Asesorias_2026' y listar bitácoras
        id_folder_2026 = drive_service.buscar_id_por_nombre(FOLDER_ASESORIAS_2026_NAME, parent_id=id_folder_asesorias, es_carpeta=True)
        archivos_bitacoras = drive_service.listar_archivos_carpeta(id_folder_2026)

        # Paso 4: Mapa de comprobación por cédula
        mapa_bitacoras = {}
        for archivo in archivos_bitacoras:
            match_cedula = re.search(r'\d+', archivo['name'])
            if match_cedula:
                cedula_extraida = match_cedula.group()
                mapa_bitacoras[cedula_extraida] = {
                    "bitacora_id": archivo['id'],
                    "nombre_archivo": archivo['name']
                }

        # Paso 5: Cruzar listado con verificación de bitácoras
        resultado = []
        for emp in lista_emprendedores:
            cedula = emp["cedula"]
            tiene_bitacora = cedula in mapa_bitacoras
            bitacora_info = mapa_bitacoras.get(cedula, {})

            resultado.append(EmpresarioResponse(
                id=emp["id"],
                cedula=cedula,
                nombre=emp["nombre"],
                empresa=emp.get("empresa", "Empresa Registrada"),
                sector=emp.get("sector", "Por Definir"),
                tiene_bitacora=tiene_bitacora,
                archivo_bitacora=bitacora_info.get("nombre_archivo", None),
                bitacora_file_id=bitacora_info.get("bitacora_id", None)
            ))

        return resultado

    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de sincronización con Google Drive: {str(e)}")
