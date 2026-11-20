#"""import os
#from google.oauth2.service_account import Credentials
#from googleapiclient.discovery import build
#import pandas as pd
#import io
#from googleapiclient.http import MediaIoBaseDownload
#
#class GoogleDriveService:
#    SCOPES = [
#        'https://www.googleapis.com/auth/drive.readonly',
#        'https://www.googleapis.com/auth/spreadsheets.readonly'
#    ]
#
#    def __init__(self):
#        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
#        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
#        self._credentials = None
#        self._drive_service = None
#
#    def _get_credentials(self):
#        if not self._credentials:
#            self._credentials = Credentials.from_service_account_file(
#                self.credentials_path, 
#                scopes=self.SCOPES
#            )
#        return self._credentials
#
#    def get_drive_client(self):
#        if not self._drive_service:
#            creds = self._get_credentials()
#            self._drive_service = build('drive', 'v3', credentials=creds)
#        return self._drive_service
#
#    def listar_bitacoras(self):
#        """
#        Consulta la carpeta configurada y extrae los archivos .xlsx de bitácoras.
#        """
#        service = self.get_drive_client()
#        query = f"'{self.folder_id}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and trashed=false"
#        
#        results = service.files().list(
#            q=query,
#            fields="files(id, name)"
#        ).execute()
#        
#        return results.get('files', [])
#
#    def leer_excel_bitacora(self, file_id: str) -> pd.DataFrame:
#        """
#        Descarga el archivo Excel desde Drive en memoria y lo convierte a pandas DataFrame.
#        """
#        service = self.get_drive_client()
#        request = service.files().get_media(fileId=file_id)
#        file_stream = io.BytesIO()
#        downloader = MediaIoBaseDownload(file_stream, request)
#        
#        done = False
#        while not done:
#            _, done = downloader.next_chunk()
#            
#        file_stream.seek(0)
#        # Lectura de la hoja principal de la bitácora
#        df = pd.read_excel(file_stream, engine='openpyxl')
#        return df
#
## Instancia singleton para reutilización
#drive_service = GoogleDriveService()"""

# 09/08/2026 cambios

# services/drive_service.py
import os
import io
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class GoogleDriveService:
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]

    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        self._credentials = None
        self._drive_service = None

    def _get_credentials(self):
        if not self._credentials:
            self._credentials = Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=self.SCOPES
            )
        return self._credentials

    def get_drive_client(self):
        if not self._drive_service:
            creds = self._get_credentials()
            self._drive_service = build('drive', 'v3', credentials=creds)
        return self._drive_service

    def buscar_id_por_nombre(self, nombre: str, parent_id: str = None, es_carpeta: bool = False) -> str:
        """
        Busca el ID único de un archivo o carpeta en Google Drive por su nombre exacto.
        """
        service = self.get_drive_client()
        query = f"name = '{nombre}' and trashed = false"
        
        if es_carpeta:
            query += " and mimeType = 'application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if not files:
            raise FileNotFoundError(f"No se encontró {'la carpeta' if es_carpeta else 'el archivo'} '{nombre}' en Google Drive.")
        
        return files[0]['id']

    def listar_archivos_carpeta(self, folder_id: str) -> list[dict]:
        """
        Devuelve todos los archivos de hoja de cálculo (.xlsx) contenidos en una carpeta específica.
        """
        service = self.get_drive_client()
        query = f"'{folder_id}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and trashed=false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=1000
        ).execute()
        
        return results.get('files', [])

    def descargar_archivo_bytes(self, file_id: str) -> bytes:
        """
        Descarga el contenido de un archivo desde Google Drive a un stream en memoria RAM.
        """
        service = self.get_drive_client()
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        
        done = False
        while not done:
            _, done = downloader.next_chunk()
            
        file_stream.seek(0)
        return file_stream.getvalue()

# Instancia Singleton para reutilización en la aplicación
drive_service = GoogleDriveService()