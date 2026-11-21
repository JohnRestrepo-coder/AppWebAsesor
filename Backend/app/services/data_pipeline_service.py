import time
import re
from datetime import datetime
from typing import Optional, List, Dict
from app.models.empresario import EmpresarioResponse, SincronizacionResponse
from app.services.drive_service import drive_service
from app.services.excel_service import excel_service
from app.utils.constants import FOLDER_ASESORIAS_NAME, FOLDER_ASESORIAS_2026_NAME, FILE_LISTA_EMPRENDEDORES_NAME

# Lista de contingencia basada en los archivos reales de Drive
EMPRESARIOS_CONTINGENCIA = [
    {
        "id": "80442045",
        "cedula": "80442045",
        "nombre": "Raúl Hernán Ortiz Beltrán",
        "empresa": "Muebles Ortiz",
        "sector": "Madera y Muebles",
        "telefono": "3154567890",
        "tiene_bitacora": True,
        "archivo_bitacora": "Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx",
        "bitacora_file_id": "mock-drive-id-80442045"
    },
    {
        "id": "29740252",
        "cedula": "29740252",
        "nombre": "María Isabel Yepes Ascensio",
        "empresa": "Confecciones El Sol",
        "sector": "Textil y Confección",
        "telefono": "3187654321",
        "tiene_bitacora": True,
        "archivo_bitacora": "Bitacora 29740252 MARIA ISABEL YEPES ASCENSIO.xlsx",
        "bitacora_file_id": "mock-drive-id-29740252"
    },
    {
        "id": "1007706965",
        "cedula": "1007706965",
        "nombre": "Stefanny Bernal Benavides",
        "empresa": "Detalles Stefanny",
        "sector": "Artesanías y Regalos",
        "telefono": "3123456789",
        "tiene_bitacora": True,
        "archivo_bitacora": "Bitacora 1007706965 STEFANNY BERNAL BENAVIDES.xlsx",
        "bitacora_file_id": "mock-drive-id-1007706965"
    },
    {
        "id": "31880769",
        "cedula": "31880769",
        "nombre": "Luz Eugenia Pérez Peña",
        "empresa": "Comercializadora Pérez",
        "sector": "Comercio Minorista",
        "telefono": "3169876543",
        "tiene_bitacora": True,
        "archivo_bitacora": "Bitacora 31880769 LUZ EUGENIA PEREZ PEÑA.xlsx",
        "bitacora_file_id": "mock-drive-id-31880769"
    },
    {
        "id": "1061777035",
        "cedula": "1061777035",
        "nombre": "Astrid Natalia Aranda Patiño",
        "empresa": "Estética Natalia",
        "sector": "Servicios y Belleza",
        "telefono": "3171122334",
        "tiene_bitacora": True,
        "archivo_bitacora": "Bitacora 1061777035 ASTRID NATALIA ARANDA PATIÑO.xlsx",
        "bitacora_file_id": "mock-drive-id-1061777035"
    }
]

class DataPipelineService:
    CACHE_TTL_SEGUNDOS = 600  # 10 minutos de caché en memoria

    def __init__(self):
        self._cache_data: Optional[List[EmpresarioResponse]] = None
        self._cache_timestamp: float = 0.0
        self._drive_status: str = "disconnected"
        self._mensaje_status: str = "Inicializando pipeline de datos..."
        self._ultima_sync: str = "Nunca"

    def _es_cache_valida(self) -> bool:
        if self._cache_data is None:
            return False
        return (time.time() - self._cache_timestamp) < self.CACHE_TTL_SEGUNDOS

    def obtener_catalogo_empresarios(self, forzar: bool = False) -> SincronizacionResponse:
        """
        Retorna la lista de empresarios utilizando la caché si es válida,
        o consultando Google Drive si ha expirado o si forzar=True.
        """
        if not forzar and self._es_cache_valida():
            return SincronizacionResponse(
                drive_status=self._drive_status,
                mensaje=f"Datos servidos desde caché en memoria (TTL restante: {int(self.CACHE_TTL_SEGUNDOS - (time.time() - self._cache_timestamp))}s)",
                ultima_sincronizacion=self._ultima_sync,
                total_empresarios=len(self._cache_data),
                empresarios=self._cache_data
            )

        # Sincronización real con Google Drive
        try:
            # Paso 1: Buscar carpeta 'Asesorias'
            id_folder_asesorias = drive_service.buscar_id_por_nombre(FOLDER_ASESORIAS_NAME, es_carpeta=True)

            # Paso 2: Descargar 'Lista Emprendedores.xlsx'
            id_excel_lista = drive_service.buscar_id_por_nombre(FILE_LISTA_EMPRENDEDORES_NAME, parent_id=id_folder_asesorias)
            bytes_lista = drive_service.descargar_archivo_bytes(id_excel_lista)
            lista_emprendedores = excel_service.procesar_hoja_emprendedores(bytes_lista)

            # Paso 3: Listar bitácoras en 'Asesorias_2026'
            id_folder_2026 = drive_service.buscar_id_por_nombre(FOLDER_ASESORIAS_2026_NAME, parent_id=id_folder_asesorias, es_carpeta=True)
            archivos_bitacoras = drive_service.listar_archivos_carpeta(id_folder_2026)

            # Paso 4: Cruzar por cédula
            mapa_bitacoras = {}
            for archivo in archivos_bitacoras:
                match = re.search(r'\d+', archivo['name'])
                if match:
                    cedula_num = match.group()
                    mapa_bitacoras[cedula_num] = {
                        "id": archivo['id'],
                        "nombre": archivo['name']
                    }

            resultado: List[EmpresarioResponse] = []
            for emp in lista_emprendedores:
                ced = emp["cedula"]
                tiene = ced in mapa_bitacoras
                info = mapa_bitacoras.get(ced, {})
                resultado.append(EmpresarioResponse(
                    id=emp["id"],
                    cedula=ced,
                    nombre=emp["nombre"],
                    empresa=emp.get("empresa", "Microempresa Registrada"),
                    sector=emp.get("sector", "Por Definir"),
                    telefono=emp.get("telefono", "3150000000"),
                    tiene_bitacora=tiene,
                    archivo_bitacora=info.get("nombre", None),
                    bitacora_file_id=info.get("id", None)
                ))

            # Actualizar caché
            self._cache_data = resultado
            self._cache_timestamp = time.time()
            self._drive_status = "connected"
            self._ultima_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._mensaje_status = "Sincronizado exitosamente con Google Drive."

        except Exception as e:
            error_str = str(e)
            print(f"⚠️ Aviso en sincronización de Google Drive: {error_str}")

            if "Google Drive API has not been used" in error_str or "accessNotConfigured" in error_str:
                self._drive_status = "api_disabled"
                self._mensaje_status = "Google Drive API pendiente de activación en Google Cloud Console."
            else:
                self._drive_status = "offline"
                self._mensaje_status = f"Modo contingencia: {error_str[:120]}"

            if self._cache_data is None:
                self._cache_data = [EmpresarioResponse(**item) for item in EMPRESARIOS_CONTINGENCIA]
                self._ultima_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._cache_timestamp = time.time()

        return SincronizacionResponse(
            drive_status=self._drive_status,
            mensaje=self._mensaje_status,
            ultima_sincronizacion=self._ultima_sync,
            total_empresarios=len(self._cache_data),
            empresarios=self._cache_data
        )

    def obtener_empresario_por_id(self, id_o_cedula: str) -> Optional[EmpresarioResponse]:
        catalogo = self.obtener_catalogo_empresarios(forzar=False)
        for emp in catalogo.empresarios:
            if emp.id == id_o_cedula or emp.cedula == id_o_cedula:
                return emp
        return None

data_pipeline_service = DataPipelineService()
