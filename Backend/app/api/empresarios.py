#from fastapi import APIRouter, HTTPException
#from services.drive_service import drive_service
#import re
#
#router = APIRouter(prefix="/api", tags=["Empresarios"])
#
#def parsear_nombre_bitacora(file_id: str, file_name: str):
#    nombre_limpio = file_name.replace(".xlsx", "").replace("xlsx", "").strip()
#    match_cedula = re.search(r'\d+', nombre_limpio)
#    
#    if match_cedula:
#        cedula = match_cedula.group()
#        partes = nombre_limpio.split(cedula)
#        nombre = partes[1].strip() if len(partes) > 1 else "Empresario"
#        nombre = re.sub(r'\b2026\b', '', nombre, flags=re.IGNORECASE).strip()
#    else:
#        cedula = "SIN_CEDULA"
#        nombre = nombre_limpio
#
#    return {
#        "id": file_id,
#        "cedula": cedula,
#        "nombre": nombre.title(),
#        "archivo_original": file_name
#    }
#
#@router.get("/empresarios")
#def obtener_empresarios():
#    try:
#        archivos = drive_service.listar_bitacoras()
#        lista_empresarios = [
#            parsear_nombre_bitacora(archivo['id'], archivo['name']) 
#            for archivo in archivos
#        ]
#        return lista_empresarios
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=f"Error al conectar con Google Drive: {str(e)}")

# api/empresarios.py
from fastapi import APIRouter, HTTPException
from services.drive_service import drive_service
from services.excel_service import excel_service
import re

router = APIRouter(prefix="/api", tags=["Empresarios"])

@router.get("/empresarios")
def obtener_empresarios():
    """
    1. Carga la lista base desde 'Mi unidad/Asesorias/Lista Emprendedores.xlsx' (Hoja Emprendedores).
    2. Comprueba la existencia de la bitácora individual en 'Mi unidad/Asesorias/Asesorias_2026/'.
    3. Retorna la información estructurada para el Frontend.
    """
    try:
        # Step 1: Obtener ID de carpeta contenedora 'Asesorias'
        id_folder_asesorias = drive_service.buscar_id_por_nombre("Asesorias", es_carpeta=True)

        # Step 2: Descargar y procesar 'Lista Emprendedores.xlsx'
        id_excel_lista = drive_service.buscar_id_por_nombre("Lista Emprendedores.xlsx", parent_id=id_folder_asesorias)
        bytes_lista = drive_service.descargar_archivo_bytes(id_excel_lista)
        lista_emprendedores = excel_service.procesar_hoja_emprendedores(bytes_lista)

        # Step 3: Obtener ID de la subcarpeta 'Asesorias_2026' y listar bitácoras
        id_folder_2026 = drive_service.buscar_id_por_nombre("Asesorias_2026", parent_id=id_folder_asesorias, es_carpeta=True)
        archivos_bitacoras = drive_service.listar_archivos_carpeta(id_folder_2026)

        # Step 4: Mapa de comprobación por cédula
        mapa_bitacoras = {}
        for archivo in archivos_bitacoras:
            match_cedula = re.search(r'\d+', archivo['name'])
            if match_cedula:
                cedula_extraida = match_cedula.group()
                mapa_bitacoras[cedula_extraida] = {
                    "bitacora_id": archivo['id'],
                    "nombre_archivo": archivo['name']
                }

        # Step 5: Cruzar listado con verificación de bitácoras
        resultado = []
        for emp in lista_emprendedores:
            cedula = emp["cedula"]
            tiene_bitacora = cedula in mapa_bitacoras
            bitacora_info = mapa_bitacoras.get(cedula, {})

            resultado.append({
                "id": emp["id"],
                "cedula": cedula,
                "nombre": emp["nombre"],
                "empresa": emp["empresa"],
                "sector": emp["sector"],
                "tiene_bitacora": tiene_bitacora,
                "archivo_bitacora": bitacora_info.get("nombre_archivo", None),
                "bitacora_file_id": bitacora_info.get("bitacora_id", None)
            })

        return resultado

    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de sincronización con Google Drive: {str(e)}")