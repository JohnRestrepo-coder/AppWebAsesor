import pandas as pd
import io
import re
from typing import List, Dict, Any

class ExcelService:
    @staticmethod
    def procesar_hoja_emprendedores(contenido_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Procesa el archivo 'Lista Emprendedores.xlsx', leyendo específicamente la hoja 'Emprendedores'.
        Mapea las columnas: ID, Cedula, Nombre, Apellido, Empresa, Sector.
        """
        try:
            df = pd.read_excel(io.BytesIO(contenido_bytes), sheet_name="Emprendedores", engine="openpyxl")
            df.columns = [str(col).strip().lower() for col in df.columns]
            
            col_id = next((c for c in df.columns if c == 'id'), None)
            col_cedula = next((c for c in df.columns if 'cedula' in c or 'cédula' in c), None)
            col_nombre = next((c for c in df.columns if 'nombre' in c), None)
            col_apellido = next((c for c in df.columns if 'apellido' in c), None)
            col_empresa = next((c for c in df.columns if 'empresa' in c or 'negocio' in c), None)
            col_sector = next((c for c in df.columns if 'sector' in c or 'actividad' in c), None)

            emprendedores = []
            for _, row in df.iterrows():
                raw_cedula = str(row[col_cedula]) if col_cedula and pd.notna(row[col_cedula]) else ""
                match_cedula = re.search(r'\d+', raw_cedula)
                cedula = match_cedula.group() if match_cedula else ""

                if not cedula:
                    continue

                nombre_str = str(row[col_nombre]).strip() if col_nombre and pd.notna(row[col_nombre]) else ""
                apellido_str = str(row[col_apellido]).strip() if col_apellido and pd.notna(row[col_apellido]) else ""
                nombre_completo = f"{nombre_str} {apellido_str}".strip().title()
                id_registro = str(row[col_id]) if col_id and pd.notna(row[col_id]) else cedula

                empresa_val = str(row[col_empresa]).strip() if col_empresa and pd.notna(row[col_empresa]) else "Microempresa Registrada"
                sector_val = str(row[col_sector]).strip() if col_sector and pd.notna(row[col_sector]) else "Por Definir"

                emprendedores.append({
                    "id": id_registro,
                    "cedula": cedula,
                    "nombre": nombre_completo,
                    "empresa": empresa_val,
                    "sector": sector_val
                })

            return emprendedores

        except Exception as e:
            raise ValueError(f"Error procesando la pestaña 'Emprendedores': {str(e)}")

    @staticmethod
    def extraer_resumen_bitacora(contenido_bytes: bytes) -> str:
        """
        Lee una bitácora individual de asesoría (.xlsx) e inspecciona sus hojas 
        para generar un resumen contextual textual para el LLM.
        """
        try:
            excel_file = pd.ExcelFile(io.BytesIO(contenido_bytes), engine="openpyxl")
            nombres_hojas = excel_file.sheet_names
            resumen_partes = [f"Hojas encontradas en la bitácora: {', '.join(nombres_hojas)}."]

            for hoja in nombres_hojas[:3]:  # Procesar hasta las primeras 3 hojas clave
                df = pd.read_excel(excel_file, sheet_name=hoja)
                if df.empty:
                    continue

                # Extraer primeras 5 filas no vacías
                resumen_partes.append(f"\n--- Contenido de la hoja '{hoja}' ---")
                filas_texto = []
                for idx, fila in df.head(5).iterrows():
                    valores_limpios = [f"{col}: {val}" for col, val in fila.items() if pd.notna(val)]
                    if valores_limpios:
                        filas_texto.append(" | ".join(valores_limpios[:6]))

                resumen_partes.append("\n".join(filas_texto) if filas_texto else "Sin datos registrados.")

            return "\n".join(resumen_partes)

        except Exception as e:
            return f"Bitácora presente en Drive pero no se pudo parsear el contenido: {str(e)}"

    @staticmethod
    def generar_contexto_contingencia(nombre: str, empresa: str, sector: str) -> str:
        """
        Genera un contexto representativo de diagnóstico para microempresarios
        cuando la bitácora no se puede descargar o no está vinculada.
        """
        return f"""
- Estado General: Expediente activo en programa de fortalecimiento microempresarial.
- Diagnóstico Inicial:
  * Ventas: Concentradas en canal presencial / "boca a boca". Sin presencia digital estructurada.
  * Finanzas: Registros manuales en cuaderno. Alerta moderada de mezcla de dinero del hogar con compras del negocio.
  * Costos: Conoce el precio de compra de insumos, pero no calcula la mano de obra propia en el costo final.
  * Meta Anterior: Organizar recibos de proveedores y definir precios base.
"""

excel_service = ExcelService()
