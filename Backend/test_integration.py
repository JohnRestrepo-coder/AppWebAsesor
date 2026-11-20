import sys
import os

# ==============================================================================
# RESOLUCIÓN DE RUTAS DEL SISTEMA (Importaciones desde app.*)
# ==============================================================================
DIRECTORIO_BACKEND = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_BACKEND not in sys.path:
    sys.path.insert(0, DIRECTORIO_BACKEND)

from app.services.drive_service import drive_service
from app.services.excel_service import excel_service

def probar_conexion_y_parseo():
    print("=" * 60)
    print("🚀 PRUEBA DE INTEGRACIÓN BACKEND - FUNDACIÓN WWB COLOMBIA")
    print("=" * 60)
    
    try:
        print("\n🔍 [PASO 1] Buscando carpeta contenedora 'Asesorias'...")
        id_asesorias = drive_service.buscar_id_por_nombre("Asesorias", es_carpeta=True)
        print(f"   ✅ Carpeta 'Asesorias' encontrada. ID: {id_asesorias}")

        print("\n🔍 [PASO 2] Descargando 'Lista Emprendedores.xlsx'...")
        id_excel = drive_service.buscar_id_por_nombre("Lista Emprendedores.xlsx", parent_id=id_asesorias)
        bytes_excel = drive_service.descargar_archivo_bytes(id_excel)
        print("   ✅ Archivo maestro descargado con éxito en memoria RAM.")

        print("\n🔍 [PASO 3] Procesando la hoja 'Emprendedores' con ExcelService...")
        emprendedores = excel_service.procesar_hoja_emprendedores(bytes_excel)
        print(f"   ✅ Se procesaron {len(emprendedores)} emprendedores exitosamente.")
        if emprendedores:
            print(f"   📌 Registro [0]: {emprendedores[0]}")

        print("\n🔍 [PASO 4] Listando contenido de la carpeta 'Asesorias_2026'...")
        id_2026 = drive_service.buscar_id_por_nombre("Asesorias_2026", parent_id=id_asesorias, es_carpeta=True)
        bitacoras = drive_service.listar_archivos_carpeta(id_2026)
        print(f"   ✅ Se encontraron {len(bitacoras)} archivos de bitácora en 'Asesorias_2026'.")

        print("\n" + "=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS DE INTEGRACIÓN DE BACKEND PASARON EXITOSAMENTE!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA PRUEBA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    probar_conexion_y_parseo()
