import re

def extraer_cedula(texto: str) -> str:
    """Extrae el primer bloque numérico correspondiente a la cédula."""
    if not texto:
        return ""
    match = re.search(r'\d+', str(texto))
    return match.group() if match else ""

def limpiar_nombre_archivo(nombre_archivo: str) -> dict:
    """
    Parsea un nombre de archivo como 'Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx'
    retornando cedula y nombre limpio.
    """
    nombre_sin_ext = nombre_archivo.replace(".xlsx", "").replace("xlsx", "").strip()
    cedula = extraer_cedula(nombre_sin_ext)
    
    if cedula:
        partes = nombre_sin_ext.split(cedula)
        nombre = partes[1].strip() if len(partes) > 1 else "Empresario"
        nombre = re.sub(r'\b2026\b', '', nombre, flags=re.IGNORECASE).strip()
    else:
        cedula = "SIN_CEDULA"
        nombre = nombre_sin_ext

    return {
        "cedula": cedula,
        "nombre": nombre.title(),
        "archivo_original": nombre_archivo
    }
