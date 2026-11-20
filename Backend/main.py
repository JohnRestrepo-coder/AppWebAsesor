# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="Backend Consultor WWB - Modo Bitácoras Individuales")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Simulación de los archivos que Python "leerá" de tu carpeta de Google Drive (Asesorias_2026)
ARCHIVOS_DRIVE_SIMULADOS = [
    "Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx",
    "Bitacora 29740252 MARIA ISABEL YEPES ASCENSIO.xlsx",
    "Bitacora 1007706965 STEFANNY BERNAL BENAVIDES.xlsx",
    "Bitacora 31880769 LUZ EUGENIA PEREZ PEÑA.xlsx",
    "Bitacora 1061777035 ASTRID NATALIA ARANDA PATIÑO.xlsx",
    "BITACORA 29939328 YOLANDA COBO GOMEZ 2026 xlsx.xlsx",
    "BITACORA 1130646618 DEISY PATRICIA BROWN LOPEZ 2026.xlsx",
    "BITACORA 31792462 MARIA FERNANDA LUNA GIRALDO.xlsx",
    "BITACORA 94486515 JORGE ELIECER OSPINA MOTATO.xlsx"
]

def procesar_nombre_archivo(nombre_archivo):
    """
    Esta función toma un nombre de archivo como 'Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx'
    y extrae automáticamente: la cédula, el nombre limpio y el ID del archivo.
    """
    # Limpiamos la extensión .xlsx e ignoramos si dice "Bitacora" o "BITACORA"
    nombre_sin_ext = nombre_archivo.replace(".xlsx", "").replace("xlsx", "").strip()
    
    # Buscamos el número de cédula (una secuencia de números)
    match_cedula = re.search(r'\d+', nombre_sin_ext)
    
    if match_cedula:
        cedula = match_cedula.group()
        # El nombre del empresario es todo lo que queda después de la cédula
        partes = nombre_sin_ext.split(cedula)
        nombre_empresario = partes[1].strip() if len(partes) > 1 else "Nombre no identificado"
        
        # Quitamos años como "2026" que puedan quedar al final del nombre
        nombre_empresario = re.sub(r'\b2026\b', '', nombre_empresario).strip()
    else:
        cedula = "Sin Cédula"
        nombre_empresario = nombre_sin_ext

    return {
        "id": cedula,  # Usaremos la cédula como ID único para hacerlo fácil
        "cedula": cedula,
        "nombre": nombre_empresario.title(), # Lo pone bonito: "Raul Hernan..."
        "archivo_original": nombre_archivo,
        "negocio": "Microempresa registrada", # Dato que luego leeremos dentro del Excel
        "sector": "Por definir en sesión",
        "problematicas": "Información dentro de la bitácora individual en Google Drive.",
        "historico_sesiones": "Bitácora lista para lectura y registro de asesoría."
    }

# Creamos nuestra lista de empresarios en tiempo real procesando los nombres de archivos
@app.get("/api/empresarios")
def obtener_empresarios():
    empresarios_procesados = [procesar_nombre_archivo(archivo) for archivo in ARCHIVOS_DRIVE_SIMULADOS]
    return empresarios_procesados

# Esquema para recibir las consultas a la IA
class ConsultaIARequest(BaseModel):
    empresario_id: str
    pregunta: str

@app.post("/api/consulta-ia")
async def consultar_ia(request: ConsultaIARequest):
    # Procesamos la lista para buscar al empresario seleccionado
    empresarios = [procesar_nombre_archivo(archivo) for archivo in ARCHIVOS_DRIVE_SIMULADOS]
    empresario = next((e for e in empresarios if e["id"] == request.empresario_id), None)
    
    if not empresario:
        raise HTTPException(status_code=404, detail="Empresario no encontrado")
    
    # Aquí es donde Python irá a Google Drive a leer el contenido de la bitácora específica:
    # "Bitacora {cedula} {nombre}.xlsx" para alimentar a Gemini con datos reales.
    
    prompt_contextualizado = f"""
    Estás analizando la bitácora individual del empresario {empresario['nombre']} con Cédula {empresario['cedula']}.
    El archivo original en Google Drive es: {empresario['archivo_original']}.
    
    Pregunta del consultor: "{request.pregunta}"
    """
    
    respuesta_simulada = (
        f"**[Gemini AI - Análisis de Bitácora Individual]**\n\n"
        f"He revisado la bitácora correspondiente al archivo **'{empresario['archivo_original']}'**.\n\n"
        f"Para responder a tu consulta sobre *'{request.pregunta}'* para el/la empresario(a) **{empresario['nombre']}**:\n"
        f"- **Recomendación:** Al tratarse de un diagnóstico de bitácora individual, sugiero abrir la pestaña de 'Estructura de costos' en su Excel y validar si el margen de contribución está alineado con el sector.\n"
        f"- **Próximo Paso:** Usa el botón de dictado de voz para guardar el resumen de esta recomendación directamente en este archivo de Google Drive."
    )
    
    return {"respuesta": respuesta_simulada}