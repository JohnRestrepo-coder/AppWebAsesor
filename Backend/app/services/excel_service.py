## services/excel_service.py
#import pandas as pd
#import io
#import re
#
#class ExcelService:
#    @staticmethod
#    def procesar_lista_emprendedores(contenido_bytes: bytes) -> list[dict]:
#        """
#        Procesa el archivo 'Lista Emprendedores.xlsx' leyendo la hoja 'Emprendedores'.
#        Extrae y normaliza: ID, Cédula, Nombre y Apellido.
#        """
#        try:
#            # Cargar la pestaña 'Emprendedores' desde el stream en memoria
#            df = pd.read_excel(io.BytesIO(contenido_bytes), sheet_name="Emprendedores", engine="openpyxl")
#            
#            # Normalizar nombres de columnas a minúsculas y sin espacios adicionales
#            df.columns = [str(col).strip().lower() for col in df.columns]
#            
#            # Identificar dinámicamente nombres de columnas principales
#            col_id = next((c for c in df.columns if c == 'id'), None)
#            col_cedula = next((c for c in df.columns if 'cedula' in c or 'cédula' in c), None)
#            col_nombre = next((c for c in df.columns if 'nombre' in c), None)
#            col_apellido = next((c for c in df.columns if 'apellido' in c), None)
#
#            emprendedores = []
#            for _, row in df.iterrows():
#                # Extracción y limpieza de la cédula
#                raw_cedula = str(row[col_cedula]) if col_cedula and pd.notna(row[col_cedula]) else ""
#                match_cedula = re.search(r'\d+', raw_cedula)
#                cedula = match_cedula.group() if match_cedula else ""
#
#                if not cedula:
#                    continue  # Saltar registros vacíos o sin cédula
#
#                nombre_raw = str(row[col_nombre]).strip() if col_nombre and pd.notna(row[col_nombre]) else ""
#                apellido_raw = str(row[col_apellido]).strip() if col_apellido and pd.notna(row[col_apellido]) else ""
#                
#                # Unificar nombre completo ordenado
#                nombre_completo = f"{nombre_raw} {apellido_raw}".strip().title()
#
#                id_registro = str(row[col_id]) if col_id and pd.notna(row[col_id]) else cedula
#
#                emprendedores.append({
#                    "id": id_registro,
#                    "cedula": cedula,
#                    "nombre": nombre_completo,
#                    "empresa": "Empresa Registrada",  # Valor por defecto
#                    "sector": "Sector por definir"    # Valor por defecto
#                })
#
#            return emprendedores
#
#        except Exception as e:
#            raise ValueError(f"Error procesando la pestaña 'Emprendedores': {str(e)}")
#
#excel_service = ExcelService()

#09/08/2026

# services/excel_service.py
import pandas as pd
import io
import re

class ExcelService:
    @staticmethod
    def procesar_hoja_emprendedores(contenido_bytes: bytes) -> list[dict]:
        """
        Procesa el archivo 'Lista Emprendedores.xlsx', leyendo específicamente la hoja 'Emprendedores'.
        Mapea las columnas: ID, Cedula, Nombre, Apellido.
        """
        try:
            # Cargar en memoria especificando la hoja requerida
            df = pd.read_excel(io.BytesIO(contenido_bytes), sheet_name="Emprendedores", engine="openpyxl")
            
            # Normalizar nombres de columnas a minúsculas
            df.columns = [str(col).strip().lower() for col in df.columns]
            
            col_id = next((c for c in df.columns if c == 'id'), None)
            col_cedula = next((c for c in df.columns if 'cedula' in c or 'cédula' in c), None)
            col_nombre = next((c for c in df.columns if 'nombre' in c), None)
            col_apellido = next((c for c in df.columns if 'apellido' in c), None)

            emprendedores = []
            for _, row in df.iterrows():
                # Extracción y limpieza de la cédula
                raw_cedula = str(row[col_cedula]) if col_cedula and pd.notna(row[col_cedula]) else ""
                match_cedula = re.search(r'\d+', raw_cedula)
                cedula = match_cedula.group() if match_cedula else ""

                if not cedula:
                    continue  # Omitir filas vacías

                nombre_str = str(row[col_nombre]).strip() if col_nombre and pd.notna(row[col_nombre]) else ""
                apellido_str = str(row[col_apellido]).strip() if col_apellido and pd.notna(row[col_apellido]) else ""
                
                # Unificar Nombre y Apellido
                nombre_completo = f"{nombre_str} {apellido_str}".strip().title()
                id_registro = str(row[col_id]) if col_id and pd.notna(row[col_id]) else cedula

                emprendedores.append({
                    "id": id_registro,
                    "cedula": cedula,
                    "nombre": nombre_completo,
                    "empresa": "Sin Registro de Empresa", # Atributo configurable
                    "sector": "Por Definir"                # Atributo configurable
                })

            return emprendedores

        except Exception as e:
            raise ValueError(f"Error procesando la pestaña 'Emprendedores': {str(e)}")

excel_service = ExcelService()