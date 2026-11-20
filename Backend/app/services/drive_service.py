# services/drive_service.py
import os
import io
from pathlib import Path
from typing import List, Dict
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class GoogleDriveService:
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]

    def __init__(self):
        creds_env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        if not os.path.isabs(creds_env):
            backend_dir = Path(__file__).resolve().parent.parent.parent
            candidate = backend_dir / creds_env
            if candidate.exists():
                self.credentials_path = str(candidate)
            else:
                self.credentials_path = creds_env
        else:
            self.credentials_path = creds_env

        self._credentials = None
        self._drive_service = None

    def _get_credentials(self):
        if not self._credentials:
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(
                    f"Archivo de credenciales no encontrado en: {self.credentials_path}. "
                    "Verifica GOOGLE_APPLICATION_CREDENTIALS en tu .env"
                )
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

    def listar_archivos_carpeta(self, folder_id: str) -> List[Dict]:
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
